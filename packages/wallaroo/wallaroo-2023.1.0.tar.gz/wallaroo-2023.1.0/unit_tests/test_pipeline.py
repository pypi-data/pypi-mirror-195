import wallaroo
from wallaroo.model import Model
from wallaroo.model_config import ModelConfig
from wallaroo.pipeline import Pipeline
from wallaroo.pipeline_variant import PipelineVariant
from wallaroo.tag import Tag

from aioresponses import aioresponses
import asyncio
import datetime
import json
import numpy
import os
import pyarrow as pa
import responses
import tempfile
import unittest
from unittest import mock

from . import testutil


with open("unit_tests/outputs/sample_inference_result.json", "r") as fp:
    SAMPLE_INFERENCE_RESULT = json.loads(fp.read())

with open("unit_tests/outputs/sample_batched_inference_result.json", "r") as fp:
    SAMPLE_BATCHED_INFERENCE_RESULT = json.loads(fp.read())


def logged_inference():
    with open("unit_tests/outputs/sample_logged_inference_result.json", "r") as fp:
        return json.loads(fp.read())


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.ix = 0
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(
            endpoint="http://api-lb:8080/v1/graphql"
        )
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth"
        )

    def gen_id(self):
        self.ix += 1
        return self.ix

    def ccfraud_model(self, variant="some_model_variant_name"):
        data = {
            "id": self.gen_id(),
            "model_id": "some_model_name",
            "model_version": variant,
            "sha": "ccfraud_sha",
            "file_name": "some_model_file.onnx",
            "updated_at": self.now.isoformat(),
            "visibility": "private",
        }

        model = Model(
            client=self.test_client,
            data=data,
        )
        model._config = ModelConfig(
            client=self.test_client,
            data={
                "id": self.gen_id(),
                "model": {
                    "id": model.id(),
                },
                "runtime": "onnx",
                "tensor_fields": "foo bar baz",
            },
        )
        model._config._model = model
        return model

    def add_pipeline_by_id_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineById")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 3,
                        "pipeline_id": "pipeline-258146-2",
                        "created_at": "2022-04-18T13:55:16.880148+00:00",
                        "updated_at": "2022-04-18T13:55:16.915664+00:00",
                        "visibility": "private",
                        "owner_id": "'",
                        "pipeline_versions": [{"id": 2}],
                        "pipeline_tags": [
                            {"tag": {"id": 1, "tag": "byhand222"}},
                            {"tag": {"id": 2, "tag": "foo"}},
                        ],
                    }
                }
            },
        )

    def add_pipeline_variant_by_id_responder(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineVariantById")],
            json={
                "data": {
                    "pipeline_version_by_pk": {
                        "id": 2,
                        "created_at": self.now.isoformat(),
                        "updated_at": self.now.isoformat(),
                        "version": "v1",
                        "definition": {
                            "id": "test-pipeline",
                            "steps": [
                                {
                                    "id": "metavalue_split",
                                    "args": [
                                        "card_type",
                                        "default",
                                        "gold",
                                        "experiment",
                                    ],
                                    "operation": "map",
                                }
                            ],
                        },
                        "pipeline": {"id": 1},
                        "deployment_pipeline_versions": [],
                    }
                }
            },
        )

    def add_pipeline_models_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineModels")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 3,
                        "deployment": {
                            "deployment_model_configs_aggregate": {
                                "nodes": [
                                    {
                                        "model_config": {
                                            "model": {
                                                "model": {"name": "ccfraud1-258146"}
                                            }
                                        }
                                    },
                                    {
                                        "model_config": {
                                            "model": {
                                                "model": {"name": "ccfraud2-258146"}
                                            }
                                        }
                                    },
                                ]
                            },
                        },
                    }
                }
            },
        )

    def add_deployment_for_pipeline_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("GetDeploymentForPipeline")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "deployment": {
                            "id": 2,
                            "deploy_id": "pipeline-258146-2",
                            "deployed": True,
                        }
                    }
                },
            },
        )

    @responses.activate
    def test_init_full_dict(self):

        pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "test-pipeline",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        self.assertEqual(1, pipeline.id())
        self.assertEqual("test-pipeline", pipeline.name())
        self.assertEqual(self.now, pipeline.create_time())
        self.assertEqual(self.now, pipeline.last_update_time())
        self.assertIsInstance(pipeline.variants()[0], PipelineVariant)

    @responses.activate
    def test_html_repr(self):

        self.add_pipeline_by_id_responder()
        self.add_deployment_for_pipeline_responder()
        self.add_pipeline_models_responder()
        self.add_pipeline_variant_by_id_responder()

        p = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "test-pipeline",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        model1 = self.ccfraud_model("one")
        model2 = self.ccfraud_model("two")
        p = p.add_model_step(model1)
        p = p.add_model_step(model2)

        hstr = p._repr_html_()
        self.assertTrue("<table>" in hstr)

    @responses.activate
    def test_rehydrate(self):

        testcases = [
            ("name", "test-pipeline"),
            ("create_time", self.now),
            ("last_update_time", self.now),
            ("variants", None),
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    "http://api-lb:8080/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("PipelineById")],
                    json={
                        "data": {
                            "pipeline_by_pk": {
                                "id": 1,
                                "pipeline_id": "test-pipeline",
                                "created_at": self.now.isoformat(),
                                "updated_at": self.now.isoformat(),
                                "pipeline_versions": [{"id": 1}],
                                "visibility": "pUbLIC",
                            }
                        },
                    },
                )

                pipeline = Pipeline(client=self.test_client, data={"id": 1})
                got_value = getattr(pipeline, method_name)()

                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                got_value = getattr(pipeline, method_name)()
                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    def test_logs(self):
        workspace_id = 1
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/api/plateau/get_topic_name",
            match=[responses.matchers.json_params_matcher({"pipeline_pk_id": 1})],
            status=200,
            json={"topic_name": "workspace-1-pipeline-x-inference"},
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("UserDefaultWorkspace")],
            json={
                "data": {
                    "user_default_workspace": [
                        {
                            "workspace": {
                                "archived": False,
                                "created_at": "2022-02-15T09:42:12.857637+00:00",
                                "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                                "name": f"Unused",
                                "id": 1,
                                "pipelines": [],
                                "models": [],
                            }
                        }
                    ]
                }
            },
        )

        responses.add(
            responses.GET,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 20},
                }
            },
        )

        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference/records",
            status=200,
            json={
                "records": [
                    '{"model_name":"x","model_version":"0002","pipeline_id":"","outputs":[{"Float":{"v":1,"dim":[1,1],"data":[-0.000041961669921875]}}],"elapsed":43059,"time":1642193935934,"original_data":{"tensor":[[0.0]]},"check_failures":[]}'
                ],
                "status": "All",
            },
            match=[responses.matchers.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )

        pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "x",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        self.assertEqual(len(pipeline.logs(20)), 1)

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "true"})
    def test_logs_with_arrow(self):
        sink = pa.BufferOutputStream()
        with pa.ipc.open_file("unit_tests/outputs/sample_logs.arrow") as reader:
            sample_log_table = reader.read_all()
            with pa.ipc.new_file(sink, sample_log_table.schema) as arrow_ipc:
                arrow_ipc.write(sample_log_table)
                arrow_ipc.close()
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/api/plateau/get_topic_name",
            match=[responses.matchers.json_params_matcher({"pipeline_pk_id": 1})],
            status=200,
            json={"topic_name": "workspace-1-pipeline-x-inference"},
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("UserDefaultWorkspace")],
            json={
                "data": {
                    "user_default_workspace": [
                        {
                            "workspace": {
                                "archived": False,
                                "created_at": "2022-02-15T09:42:12.857637+00:00",
                                "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                                "name": f"Unused",
                                "id": 1,
                                "pipelines": [],
                                "models": [],
                            }
                        }
                    ]
                }
            },
        )

        responses.add(
            responses.GET,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 20},
                }
            },
        )

        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference/records",
            status=200,
            body=sink.getvalue(),
            match=[responses.matchers.json_params_matcher({"testing-1": 0, "testing-2": 0})],
        )

        pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "x",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )
        log_table = pipeline.logs(arrow=True)
        self.assertIsInstance(log_table, pa.Table)
        log_table.equals(sample_log_table)


    @responses.activate
    def test_log_time_shift(self):
        workspace_name = "test-logs-workspace"
        workspace_id = 1
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/api/plateau/get_topic_name",
            match=[responses.json_params_matcher({"pipeline_pk_id": 1})],
            status=200,
            json={"topic_name": "workspace-1-pipeline-x-inference"},
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("UserDefaultWorkspace")],
            json={
                "data": {
                    "user_default_workspace": [
                        {
                            "workspace": {
                                "archived": False,
                                "created_at": "2022-02-15T09:42:12.857637+00:00",
                                "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                                "name": f"{workspace_name}",
                                "id": workspace_id,
                                "pipelines": [],
                                "models": [],
                            }
                        }
                    ]
                }
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("GetDeploymentForPipeline")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "deployment": {
                            "id": 1,
                            "deploy_id": "some-pipeline",
                            "deployed": False,
                        }
                    }
                }
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("DeploymentById")],
            json={
                "data": {
                    "deployment_by_pk": {
                        "id": 1,
                        "deploy_id": "some-pipeline",
                        "deployed": False,
                    },
                },
            },
        )

        topic = f"workspace-{workspace_id}-pipeline-x-inference"
        responses.add(
            responses.GET,
            f"http://api-lb:8080/v1/logs/topic/{topic}",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 20},
                }
            },
        )

        prior = logged_inference()
        prior["time"] = SAMPLE_INFERENCE_RESULT[0]["time"] - 1
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/{topic}/records",
            status=200,
            json={"records": [json.dumps(prior)], "status": "All"},
            match=[responses.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )
        ready = logged_inference()
        ready["time"] = SAMPLE_INFERENCE_RESULT[0]["time"]
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/{topic}/records",
            status=200,
            json={"records": [json.dumps(prior), json.dumps(ready)], "status": "All"},
            match=[responses.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )

        responses.add(
            responses.POST,
            f"http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            status=200,
            json=SAMPLE_INFERENCE_RESULT,
        )

        pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "x",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        pipeline.infer({})

        self.assertEqual(len(pipeline.logs(20)), 2)

    @responses.activate
    def test_pipeline_building(self):
        p = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "x",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        model = self.ccfraud_model()
        p = p.add_model_step(model)
        p = p.add_validation("no_high_fraud", model.outputs[0][0] < 0.95)
        p = p.add_validation(
            "really_no_high_fraud", model.config().outputs[0][0] < 0.95
        )

        self.assertEqual(len(p.steps()), 3)

    # This can't work yet
    # def test_pipeline_clear(self):
    #     pipeline = Pipeline(
    #         client=self.test_client,
    #         data={
    #             "id": 1,
    #             "pipeline_id": "x",
    #             "created_at": self.now.isoformat(),
    #             "updated_at": self.now.isoformat(),
    #             "pipeline_versions": [{"id": 1}],
    #             "visibility": "PUBLIC",
    #         },
    #     )
    #     one = self.ccfraud_model("one")
    #     two = self.ccfraud_model("two")
    #     pipeline.add_model_step(one)
    #     pipeline.add_model_step(two)
    #     self.assertEqual(len(pipeline.steps()), 2)
    #     self.assertEqual(len(pipeline.model_configs()), 2)

    #     result = pipeline.clear()
    #     assert isinstance(result, Pipeline)
    #     self.assertEqual(pipeline.steps(), [])
    #     self.assertEqual(pipeline.model_configs(), [])

    @responses.activate
    def test_pipeline_tags(self):

        tag_1 = Tag(client=self.test_client, data={"id": 1, "tag": "bartag314"})
        tag_2 = Tag(client=self.test_client, data={"id": 2, "tag": "footag123"})

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineById")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 1,
                        "pipeline_id": "test-pipeline",
                        "created_at": self.now.isoformat(),
                        "updated_at": self.now.isoformat(),
                        "pipeline_versions": [{"id": 1}],
                        "visibility": "pUbLIC",
                        "pipeline_tags": [
                            {"tag": {"id": 1, "tag": "bartag314"}},
                            {"tag": {"id": 2, "tag": "footag123"}},
                        ],
                    }
                },
            },
        )

        pipeline = Pipeline(client=self.test_client, data={"id": 1})
        self.assertListEqual(list(map(vars, [tag_1, tag_2])), list(map(vars, pipeline.tags())))
