# Copyright (c) Recommenders contributors.
# Licensed under the MIT License.

import pytest
import papermill as pm
import scrapbook as sb


TOL = 0.05
ABS_TOL = 0.05


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, expected_values",
    [
        (
            "1m",
            {
                "map": 0.060579,
                "ndcg": 0.299245,
                "precision": 0.270116,
                "recall": 0.104350,
            },
        ),
        (
            "10m",
            {
                "map": 0.098745,
                "ndcg": 0.319625,
                "precision": 0.275756,
                "recall": 0.154014,
            },
        ),
    ],
)
def test_sar_single_node_functional(
    notebooks, output_notebook, kernel_name, size, expected_values
):
    notebook_path = notebooks["sar_single_node"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE=size),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, expected_values",
    [
        (
            "1m",
            {
                "map": 0.033914,
                "ndcg": 0.231570,
                "precision": 0.211923,
                "recall": 0.064663,
            },
        ),
        # ("10m", {"map": , "ndcg": , "precision": , "recall": }), # OOM on test machine
    ],
)
def test_baseline_deep_dive_functional(
    notebooks, output_notebook, kernel_name, size, expected_values
):
    notebook_path = notebooks["baseline_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE=size),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, expected_values",
    [
        (
            "1m",
            dict(
                rmse=0.89,
                mae=0.70,
                rsquared=0.36,
                exp_var=0.36,
                map=0.011,
                ndcg=0.10,
                precision=0.093,
                recall=0.025,
            ),
        ),
        # 10m works but takes too long
    ],
)
def test_surprise_svd_functional(
    notebooks, output_notebook, kernel_name, size, expected_values
):
    notebook_path = notebooks["surprise_svd_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(MOVIELENS_DATA_SIZE=size),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, expected_values",
    [
        (
            "1m",
            dict(
                rmse=0.959885,
                mae=0.690133,
                rsquared=0.264014,
                exp_var=0.264417,
                map=0.004857,
                ndcg=0.055128,
                precision=0.061142,
                recall=0.017789,
            ),
        )
    ],
)
@pytest.mark.skip(reason="VW pip package has installation incompatibilities")
def test_vw_deep_dive_functional(
    notebooks, output_notebook, kernel_name, size, expected_values
):
    notebook_path = notebooks["vowpal_wabbit_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(MOVIELENS_DATA_SIZE=size, TOP_K=10),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.skip(reason="NNI pip package has installation incompatibilities")
def test_nni_tuning_svd(notebooks, output_notebook, kernel_name, tmp):
    notebook_path = notebooks["nni_tuning_svd"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(
            MOVIELENS_DATA_SIZE="100k",
            SURPRISE_READER="ml-100k",
            TMP_DIR=tmp,
            MAX_TRIAL_NUM=1,
            NUM_EPOCHS=1,
            WAITING_TIME=20,
            MAX_RETRIES=50,
        ),
    )


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, expected_values",
    [
        ("1m", dict(map=0.081390, ndcg=0.406627, precision=0.373228, recall=0.132444)),
        # 10m works but takes too long
    ],
)
def test_cornac_bpr_functional(
    notebooks, output_notebook, kernel_name, size, expected_values
):
    notebook_path = notebooks["cornac_bpr_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(MOVIELENS_DATA_SIZE=size),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, epochs, expected_values",
    [
        (
            "100k",
            10,
            dict(
                eval_precision=0.131601,
                eval_recall=0.038056,
                eval_precision2=0.145599,
                eval_recall2=0.051338,
            ),
        ),
    ],
)
def test_lightfm_functional(
    notebooks, output_notebook, kernel_name, size, epochs, expected_values
):
    notebook_path = notebooks["lightfm_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(MOVIELENS_DATA_SIZE=size, NO_EPOCHS=epochs),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.experimental
@pytest.mark.parametrize(
    "expected_values",
    [({"rmse": 0.4969, "mae": 0.4761})],
)
def test_geoimc_functional(notebooks, output_notebook, kernel_name, expected_values):
    notebook_path = notebooks["geoimc_quickstart"]
    pm.execute_notebook(notebook_path, output_notebook, kernel_name=kernel_name)
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.experimental
def test_xlearn_fm_functional(notebooks, output_notebook, kernel_name):
    notebook_path = notebooks["xlearn_fm_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(LEARNING_RATE=0.2, EPOCH=10),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]

    assert results["auc_score"] == pytest.approx(0.75, rel=TOL, abs=ABS_TOL)


@pytest.mark.notebooks
@pytest.mark.parametrize(
    "size, algos, expected_values_ndcg",
    [
        (["100k"], ["svd", "sar", "bpr"], [0.094444, 0.393818, 0.444990]),
    ],
)
def test_benchmark_movielens_cpu(
    notebooks, output_notebook, kernel_name, size, algos, expected_values_ndcg
):
    notebook_path = notebooks["benchmark_movielens"]
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        kernel_name=kernel_name,
        parameters=dict(data_sizes=size, algorithms=algos),
    )
    results = sb.read_notebook(output_notebook).scraps.dataframe.set_index("name")[
        "data"
    ]
    assert len(results["results"]) == 3
    for i, value in enumerate(results["results"]):
        assert results["results"][i] == pytest.approx(value, rel=TOL, abs=ABS_TOL)
