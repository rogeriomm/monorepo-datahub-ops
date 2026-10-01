# Jupyter MCP integration test

This test uses the MCP server that is already installed and running inside the
existing `jupyter-spark-4.1` Docker Compose service. It does not install, build,
start, restart, or reconfigure an MCP server.

The service and MCP identifiers are similar but serve different purposes:

| Component              | Identifier                                    |
| ---------------------- | --------------------------------------------- |
| Docker Compose service | `jupyter-spark-4.1`                           |
| Docker container       | `jupyter_spark_4_1`                           |
| Codex MCP server       | `jupyter_spark_4_1`                           |
| MCP endpoint           | `http://jupyter-spark-4-1.localhost:8080/mcp` |

The Compose service builds the MCP packages into its Jupyter image and starts
the server as a Jupyter extension. Codex connects to that existing server using
the project configuration in [`.codex/config.toml`](../../.codex/config.toml).
Project-scoped MCP configuration is loaded only when the repository is trusted.
See the
[official Codex MCP documentation](https://developers.openai.com/codex/extend/mcp)
for general client configuration behavior.

## Prerequisites

- The existing `jupyter-spark-4.1` Compose service and Traefik are running.
- The `jupyter-spark-4.1` service is healthy.
- Codex was started from this trusted repository after the service became
  available.
- JupyterLab is open in a browser only when frontend-command coverage is
  required. Core MCP tests do not require an attached frontend.

Confirm the current service state without rebuilding or recreating it:

```shell
docker compose -f on-premises/docker/docker-compose.yaml \
  ps jupyter-spark-4.1
```

## Comprehensive Codex test

Open the browser, refresh page: http://jupyter-spark-4-1.localhost:8080

Start a new Codex session and use this prompt:

```text
Perform a comprehensive integration test of the configured
`jupyter_spark_4_1` MCP server hosted by the existing, running Docker Compose
service `jupyter-spark-4.1`.

Strict rules:
- Use the existing MCP connection only.
- Do not install, build, start, restart, replace, or reconfigure the MCP server.
- Do not run or manage Docker Compose services or containers.
- Use only tools from the `jupyter_spark_4_1` MCP server.
- Do not use shell/terminal tools, repository-reading tools, or another MCP server.
- Do not modify any existing notebook.
- Do not install packages, access external networks, inspect credentials, or read secrets.
- Continue after individual failures and record each failure.
- Request required tool approvals normally.

Test artifact:
- Start with `jupyter-mcp-complete-test.ipynb`.
- Use `list_files` first. If that filename exists, choose a unique numbered suffix.
- Leave the test notebook in place for inspection unless a safe MCP file-deletion tool is explicitly available.

Run these phases:

1. Discovery and connectivity
- List the available tools exposed by this MCP server.
- Call `list_kernels`.
- Call `list_notebooks`.
- Call `list_files` at the Jupyter root with a small depth and limit.
- Confirm that successful calls use the existing `jupyter_spark_4_1` MCP
  connection, not another server.

2. Notebook lifecycle
- Create and activate the isolated notebook using `use_notebook` in create mode.
- Call `list_notebooks` and verify that it is registered.
- Call `list_kernels` and identify its kernel.
- Open it with `docmanager_open` if that tool is available.

3. Cell insertion and reading
- Insert a Markdown cell containing:
  `# Jupyter MCP complete integration test`
- Insert a raw cell containing:
  `MCP_RAW_TEST`
- Insert a code cell containing:
  `print("MCP_EXECUTE_CELL_OK", 6 * 7)`
- Use `read_notebook` in brief mode.
- Use `read_notebook` in detailed mode.
- Use `read_cell` for representative cells if available.
- Prefer returned cell IDs over cell indexes for later operations.

4. Execution and streamed notifications
- Execute the code cell with `execute_cell`; require output containing:
  `MCP_EXECUTE_CELL_OK 42`
- Use `insert_execute_code_cell` with streaming enabled, a progress interval
  of 1 second, and a timeout of 60 seconds. Insert this code:

  import time
  print("MCP_STREAM_START")
  for step in range(3):
      print(f"MCP_STREAM_STEP={step}")
      time.sleep(1)
  print("MCP_STREAM_OK")

- Verify that execution completes and the final output contains
  `MCP_STREAM_OK`.
- Note whether progress/notification messages were accepted without JSON-RPC
  or SSE transport errors.
- Call `execute_code` with:
  `print("MCP_DIRECT_OK", sum(range(7)))`
- Verify output containing `MCP_DIRECT_OK 21`.

5. Notebook editing
For each operation, read the affected cell afterward and verify the change:
- Use `edit_cell_source` to change `MCP_RAW_TEST` to `MCP_RAW_EDITED`.
- Use `overwrite_cell_source` on a disposable cell.
- Insert a disposable Markdown cell.
- Move the disposable cell to another position using `move_cell`.
- Delete only that disposable cell using `delete_cell`.
- Execute a code cell, clear its output using `clear_cell_output`, and confirm
  that its source remains while its output and execution count are cleared.
- If any of these tools are not exposed, mark them as `NOT EXPOSED` rather
  than treating that as a transport failure.

6. Spark validation
- Insert and execute this code with a timeout of 180 seconds and streaming
  enabled:

  from pyspark.sql import SparkSession
  spark = SparkSession.builder.getOrCreate()
  total = spark.range(5).selectExpr("sum(id) AS total").first()["total"]
  print("MCP_SPARK_OK", spark.version, total)

- Require output containing `MCP_SPARK_OK` and a total of `10`.
- Report the Spark version.
- If Spark fails, capture the concise exception without attempting package
  installation or environment repair.

7. JupyterLab frontend tools
These tests require an attached JupyterLab frontend. Test each tool only if it
is exposed:
- `notebook_get_selected_cell`
- Select next cell, then select previous cell.
- Start document search with `searchText` set to `MCP_STREAM_OK`.
- Highlight the next and previous matches.
- Navigate the file browser to the test notebook’s directory.
- Refresh the file browser.
- Toggle hidden files twice so the original state is restored.
- Toggle the left area twice.
- Toggle the right area twice.
- Toggle presentation mode twice.
- Open the File, Edit, and Help menus.
- Do not change the theme unless the original theme can be determined and
  restored afterward.

If a frontend command reports that no JupyterLab client is connected, classify
it as `FRONTEND UNAVAILABLE`, not as a core MCP server failure.

8. Run-all and kernel lifecycle
- Run all notebook cells using `notebook_run-all-cells`, if exposed.
- Re-read the notebook and verify expected outputs.
- Restart the notebook kernel using `restart_notebook`, if exposed.
- After restart, execute:
  `print("MCP_RESTART_OK", 40 + 2)`
- Require output containing `MCP_RESTART_OK 42`.

9. Disconnect
- Call `unuse_notebook`.
- Call `list_notebooks` again and verify that the notebook is no longer active.
- Call `list_kernels` and report the resulting kernel state.
- Confirm with `list_files` that the test artifact was saved.

10. Final report
Produce a table containing:
- Phase
- Tool
- PASS, FAIL, NOT EXPOSED, or FRONTEND UNAVAILABLE
- Concise evidence or error

Conclude with:
- Core MCP transport status
- Notebook CRUD/editing status
- Code execution status
- Streaming-notification status
- Spark status and version
- JupyterLab frontend status
- Kernel lifecycle status
- Test notebook path
- Exact list of failed or unavailable tools
- Overall result: PASS, PARTIAL PASS, or FAIL

Do not claim PASS unless every mandatory core operation succeeded:
`list_kernels`, `list_notebooks`, `list_files`, `use_notebook`,
`insert_cell`, `read_notebook`, `execute_cell`,
`insert_execute_code_cell`, `execute_code`, and `unuse_notebook`.
```

The prompt leaves `jupyter-mcp-complete-test.ipynb`, or its numbered fallback, in the repository root for inspection. Remove that exact test file manually after reviewing the results.
The browser update in real time as Codex execute the prompt task:

![JupyterLab updating while Codex runs the MCP integration test](attachments/Pasted%20image%2020261001094324.png)

Codex output:

#### Complete MCP command transcript

**Codex**

> I’ll exercise only the existing `jupyter_spark_4_1` MCP connection, starting with its `list_files` tool and preserving the isolated notebook afterward. I’ll continue through individual failures and classify frontend-only issues separately.

The server exposed 32 tools: `application_toggle_left_area`, `application_toggle_presentation_mode`, `application_toggle_right_area`, `clear_cell_output`, `delete_cell`, `docmanager_open`, `docmanager_open_browser_tab`, `documentsearch_highlightNext`, `documentsearch_highlightPrevious`, `documentsearch_start`, `documentsearch_startWithReplace`, `edit_cell_source`, `execute_cell`, `execute_code`, `filebrowser_go_to_path`, `filebrowser_refresh`, `filebrowser_toggle_hidden_files`, `insert_cell`, `insert_execute_code_cell`, `list_files`, `list_kernels`, `list_notebooks`, `move_cell`, `notebook_get_selected_cell`, `notebook_run_all_cells`, `notebook_select_next_modified_cell`, `overwrite_cell_source`, `read_cell`, `read_notebook`, `restart_notebook`, `unuse_notebook`, and `use_notebook`.

1. **`mcp.jupyter_spark_4_1.list_files`**
   - Request: `{"path":"","max_depth":2,"limit":100}`
   - Result: `Showing 0-100 of 332 files`; the root listing succeeded.

**Codex**

> The root listing succeeded over `jupyter_spark_4_1`; I’m now resolving a collision-free notebook name and capturing the initial notebook/kernel state.

2. **`mcp.jupyter_spark_4_1.list_files`**
   - Request: `{"path":"","max_depth":4,"limit":100,"pattern":"jupyter-mcp-complete-test*.ipynb"}`
   - Result: `FAIL` — `max_depth` must be less than or equal to 3.
3. **`mcp.jupyter_spark_4_1.list_kernels`**
   - Request: `{}`
   - Result: `No kernels found on the Jupyter server.`
4. **`mcp.jupyter_spark_4_1.list_notebooks`**
   - Request: `{}`
   - Result: Five notebooks were registered; `default` was active and the four S3 notebooks had dead kernels.
5. **`mcp.jupyter_spark_4_1.list_files`**
   - Request: `{"path":"","max_depth":3,"limit":100,"pattern":"jupyter-mcp-complete-test*.ipynb"}`
   - Result: `No files matching pattern 'jupyter-mcp-complete-test*.ipynb' found in path 'root'`.
6. **`mcp.jupyter_spark_4_1.use_notebook`**
   - Request: `{"mode":"create","notebook_name":"jupyter-mcp-complete-test.ipynb","notebook_path":"jupyter-mcp-complete-test.ipynb"}`
   - Result: Connected to kernel `946ba74f-5492-4624-9d66-fc225893c6c1` and activated the new one-cell notebook.
7. **`mcp.jupyter_spark_4_1.list_notebooks`**
   - Request: `{}`
   - Result: `jupyter-mcp-complete-test.ipynb` was registered, active, and attached to an alive kernel.
8. **`mcp.jupyter_spark_4_1.list_kernels`**
   - Request: `{}`
   - Result: Kernel `946ba74f-5492-4624-9d66-fc225893c6c1`, Python 3, state `starting`.
9. **`mcp.jupyter_spark_4_1.docmanager_open`**
   - Request: `{"path":"jupyter-mcp-complete-test.ipynb"}`
   - Result: Returned the opened JupyterLab notebook widget and document context for `jupyter-mcp-complete-test.ipynb`.

**Codex**

> Notebook creation and registration passed, with kernel `946ba74f-…` alive/starting and an attached JupyterLab frontend. Next I’m building and reading the test cells before execution.

10. **`mcp.jupyter_spark_4_1.insert_cell`**
    - Request: `{"cell_index":-1,"cell_type":"markdown","cell_source":"# Jupyter MCP complete integration test","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Markdown cell inserted at index 1.
11. **`mcp.jupyter_spark_4_1.insert_cell`**
    - Request: `{"cell_index":-1,"cell_type":"raw","cell_source":"MCP_RAW_TEST","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Raw cell inserted at index 2.
12. **`mcp.jupyter_spark_4_1.insert_cell`**
    - Request: `{"cell_index":-1,"cell_type":"code","cell_source":"print(\"MCP_EXECUTE_CELL_OK\", 6 * 7)","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Code cell inserted at index 3.
13. **`mcp.jupyter_spark_4_1.read_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","response_format":"brief","limit":20}`
    - Result: Four cells returned with the expected Markdown, raw, and code first lines.
14. **`mcp.jupyter_spark_4_1.read_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","response_format":"detailed","limit":20}`
    - Result: Four cells returned with their complete expected sources.
15. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":1,"include_outputs":true}`
    - Result: `# Jupyter MCP complete integration test`.
16. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":2,"include_outputs":true}`
    - Result: `MCP_RAW_TEST`.
17. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":3,"include_outputs":true}`
    - Result: `print("MCP_EXECUTE_CELL_OK", 6 * 7)` with no execution count yet.
18. **`mcp.jupyter_spark_4_1.execute_cell`**
    - Request: `{"cell_index":3,"timeout":60,"stream":true,"progress_interval":1}`
    - Result: `MCP_EXECUTE_CELL_OK 42`.
19. **`mcp.jupyter_spark_4_1.insert_execute_code_cell`**
    - Request:

      ```json
      {
        "cell_index": 4,
        "cell_source": "import time\nprint(\"MCP_STREAM_START\")\nfor step in range(3):\n    print(f\"MCP_STREAM_STEP={step}\")\n    time.sleep(1)\nprint(\"MCP_STREAM_OK\")",
        "stream": true,
        "progress_interval": 1,
        "timeout": 60
      }
      ```

    - Streamed result:

      ```text
      MCP_STREAM_START
      MCP_STREAM_STEP=0
      MCP_STREAM_STEP=1
      MCP_STREAM_STEP=2
      MCP_STREAM_OK
      ```

20. **`mcp.jupyter_spark_4_1.execute_code`**
    - Request: `{"code":"print(\"MCP_DIRECT_OK\", sum(range(7)))","timeout":60,"progress_interval":1}`
    - Result: `MCP_DIRECT_OK 21`.

**Codex**

> All three execution paths passed: saved-cell output `42`, streamed output completed cleanly, and direct output returned `21`. I’m now validating each edit operation with an immediate readback.

21. **`mcp.jupyter_spark_4_1.edit_cell_source`**
    - Request: `{"cell_index":2,"old_string":"MCP_RAW_TEST","new_string":"MCP_RAW_EDITED","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Cell 2 changed from `MCP_RAW_TEST` to `MCP_RAW_EDITED`.
22. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":2,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `MCP_RAW_EDITED`.
23. **`mcp.jupyter_spark_4_1.insert_cell`**
    - Request: `{"cell_index":-1,"cell_type":"raw","cell_source":"MCP_OVERWRITE_BEFORE","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Disposable raw cell inserted at index 5.
24. **`mcp.jupyter_spark_4_1.overwrite_cell_source`**
    - Request: `{"cell_index":5,"cell_source":"MCP_OVERWRITE_AFTER","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Cell 5 changed from `MCP_OVERWRITE_BEFORE` to `MCP_OVERWRITE_AFTER`.
25. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":5,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `MCP_OVERWRITE_AFTER`.
26. **`mcp.jupyter_spark_4_1.insert_cell`**
    - Request: `{"cell_index":-1,"cell_type":"markdown","cell_source":"MCP_DISPOSABLE_MARKDOWN","notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Disposable Markdown cell inserted at index 6.
27. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":6,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `MCP_DISPOSABLE_MARKDOWN`.
28. **`mcp.jupyter_spark_4_1.move_cell`**
    - Request: `{"source_index":6,"target_index":1,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Markdown cell moved successfully from index 6 to index 1.
29. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":1,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Moved cell contained `MCP_DISPOSABLE_MARKDOWN`.
30. **`mcp.jupyter_spark_4_1.delete_cell`**
    - Request: `{"cell_indices":[1],"include_source":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Cell 1 deleted; returned source `MCP_DISPOSABLE_MARKDOWN`.
31. **`mcp.jupyter_spark_4_1.read_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","response_format":"brief","limit":20}`
    - Result: Six cells remained and the disposable Markdown cell was absent.
32. **`mcp.jupyter_spark_4_1.execute_cell`**
    - Request: `{"cell_index":3,"timeout":60}`
    - Result: `MCP_EXECUTE_CELL_OK 42`.
33. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":3,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Source remained present, execution count was 4, and output was `MCP_EXECUTE_CELL_OK 42`.
34. **`mcp.jupyter_spark_4_1.clear_cell_output`**
    - Request: `{"cell_index":3,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `Cell 3 output cleared successfully (1 output(s) removed).`
35. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"cell_index":3,"include_outputs":true,"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: Source remained present; execution count was `N/A` and no output remained.

**Codex**

> Editing, movement, deletion, and output clearing all verified by readback. I’m starting the 180-second Spark validation now; this may take a little longer while Spark initializes.

36. **`mcp.jupyter_spark_4_1.insert_execute_code_cell`**
    - Request:

      ```json
      {
        "cell_index": 6,
        "cell_source": "from pyspark.sql import SparkSession\nspark = SparkSession.builder.getOrCreate()\ntotal = spark.range(5).selectExpr(\"sum(id) AS total\").first()[\"total\"]\nprint(\"MCP_SPARK_OK\", spark.version, total)",
        "stream": true,
        "progress_interval": 1,
        "timeout": 180
      }
      ```

    - Result: `MCP_SPARK_OK 4.1.3 10`.

**Codex**

> Spark passed with version `4.1.3` and total `10`. The attached frontend is responsive, so I’m testing the exposed JupyterLab commands while restoring every toggled UI state.

37. **`mcp.jupyter_spark_4_1.notebook_get_selected_cell`**
    - Request: `{}`
    - Result: `{"success":true,"cellType":"markdown","cellIndex":0,"source":"New Notebook Created by Jupyter MCP Server","metadata":{},"executionCount":null}`.
38. **`mcp.jupyter_spark_4_1.documentsearch_start`**
    - Request: `{"searchText":"MCP_STREAM_OK"}`
    - Result: `Tool executed successfully`.
39. **`mcp.jupyter_spark_4_1.documentsearch_highlightNext`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
40. **`mcp.jupyter_spark_4_1.documentsearch_highlightPrevious`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
41. **`mcp.jupyter_spark_4_1.filebrowser_go_to_path`**
    - Request: `{"path":""}`
    - Result: `Tool executed successfully`.
42. **`mcp.jupyter_spark_4_1.filebrowser_refresh`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
43. **`mcp.jupyter_spark_4_1.filebrowser_toggle_hidden_files`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
44. **`mcp.jupyter_spark_4_1.filebrowser_toggle_hidden_files`**
    - Request: `{}`
    - Result: `Tool executed successfully`; original hidden-files state restored.
45. **`mcp.jupyter_spark_4_1.application_toggle_left_area`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
46. **`mcp.jupyter_spark_4_1.application_toggle_left_area`**
    - Request: `{}`
    - Result: `Tool executed successfully`; original left-area state restored.
47. **`mcp.jupyter_spark_4_1.application_toggle_right_area`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
48. **`mcp.jupyter_spark_4_1.application_toggle_right_area`**
    - Request: `{}`
    - Result: `Tool executed successfully`; original right-area state restored.
49. **`mcp.jupyter_spark_4_1.application_toggle_presentation_mode`**
    - Request: `{}`
    - Result: `Tool executed successfully`.
50. **`mcp.jupyter_spark_4_1.application_toggle_presentation_mode`**
    - Request: `{}`
    - Result: `Tool executed successfully`; original presentation-mode state restored.
51. **`mcp.jupyter_spark_4_1.notebook_run_all_cells`**
    - Request: `{}`
    - Result: `True`.
52. **`mcp.jupyter_spark_4_1.read_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","response_format":"detailed","limit":20}`
    - Result: Seven cells returned; code-cell execution counts were 6, 7, and 8.
53. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":3,"include_outputs":true}`
    - Result: `MCP_EXECUTE_CELL_OK 42`, execution count 6.
54. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":4,"include_outputs":true}`
    - Result: Stream output contained `MCP_STREAM_START`, steps 0–2, and `MCP_STREAM_OK`; execution count 7.
55. **`mcp.jupyter_spark_4_1.read_cell`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb","cell_index":6,"include_outputs":true}`
    - Result: `MCP_SPARK_OK 4.1.3 10`, execution count 8.

**Codex**

> Frontend commands and run-all passed; readback confirmed all expected outputs. I’m restarting the notebook kernel next, then validating post-restart execution and the new kernel state.

56. **`mcp.jupyter_spark_4_1.restart_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `Notebook 'jupyter-mcp-complete-test.ipynb' kernel restarted successfully. Memory state and imported packages have been cleared.`
57. **`mcp.jupyter_spark_4_1.list_kernels`**
    - Request: `{}`
    - Result: Kernel `946ba74f-5492-4624-9d66-fc225893c6c1` was `idle` with one connection.
58. **`mcp.jupyter_spark_4_1.execute_code`**
    - Request: `{"code":"print(\"MCP_RESTART_OK\", 40 + 2)","timeout":60,"progress_interval":1}`
    - Result: `MCP_RESTART_OK 42`.
59. **`mcp.jupyter_spark_4_1.unuse_notebook`**
    - Request: `{"notebook_name":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `Notebook 'jupyter-mcp-complete-test.ipynb' unused successfully. Current notebook switched to 'default'.`
60. **`mcp.jupyter_spark_4_1.list_notebooks`**
    - Request: `{}`
    - Result: The test notebook no longer appeared in the active registry; `default` was active.
61. **`mcp.jupyter_spark_4_1.list_kernels`**
    - Request: `{}`
    - Result: Kernel `946ba74f-5492-4624-9d66-fc225893c6c1` remained `idle` with one frontend connection.
62. **`mcp.jupyter_spark_4_1.list_files`**
    - Request: `{"path":"","max_depth":1,"limit":50,"pattern":"jupyter-mcp-complete-test.ipynb"}`
    - Result: `jupyter-mcp-complete-test.ipynb` existed at the Jupyter root, type `notebook`, size 2.9 KB.

**Codex**

> The notebook disconnected cleanly, disappeared from the active registry, and remains saved at the Jupyter root. I’m consolidating the per-tool evidence now, including the recovered validation error and optional commands that were not exposed.

#### Final report

Integration test completed using only the existing `jupyter_spark_4_1` MCP connection.

| Phase | Tool | Status | Evidence / error |
|---|---|---:|---|
| Discovery | Tool inventory | PASS | 32 `jupyter_spark_4_1` tools enumerated. |
| Discovery | `list_files` | PASS | Root listing returned 332 entries; valid artifact search completed. |
| Discovery | `list_files` validation attempt | FAIL | `max_depth=4` rejected because maximum is 3; retried successfully with 3. |
| Discovery | `list_kernels` | PASS | Initial state contained no running kernels. |
| Discovery | `list_notebooks` | PASS | Returned five pre-existing registrations. |
| Lifecycle | `use_notebook` | PASS | Created and activated `jupyter-mcp-complete-test.ipynb`. |
| Lifecycle | `list_notebooks` | PASS | Test notebook registered as active with an alive kernel. |
| Lifecycle | `list_kernels` | PASS | Kernel `946ba74f-5492-4624-9d66-fc225893c6c1` identified. |
| Lifecycle | `docmanager_open` | PASS | Notebook opened through the attached JupyterLab frontend. |
| Cells | `insert_cell` | PASS | Markdown, raw, and code cells inserted successfully. |
| Cells | `read_notebook` brief | PASS | Correct four-cell structure returned. |
| Cells | `read_notebook` detailed | PASS | Full sources and cell types matched. |
| Cells | `read_cell` | PASS | Representative Markdown, raw, and code cells verified. |
| Execution | `execute_cell` | PASS | Output: `MCP_EXECUTE_CELL_OK 42`. |
| Streaming | `insert_execute_code_cell` | PASS | Streamed steps 0–2 and completed with `MCP_STREAM_OK`. |
| Execution | `execute_code` | PASS | Output: `MCP_DIRECT_OK 21`. |
| Editing | `edit_cell_source` | PASS | Raw source changed to `MCP_RAW_EDITED`; readback matched. |
| Editing | `overwrite_cell_source` | PASS | Disposable raw cell changed to `MCP_OVERWRITE_AFTER`. |
| Editing | `move_cell` | PASS | Disposable Markdown cell moved from index 6 to 1. |
| Editing | `delete_cell` | PASS | Only `MCP_DISPOSABLE_MARKDOWN` was deleted. |
| Editing | `clear_cell_output` | PASS | Source remained; output removed and execution count became `N/A`. |
| Spark | `insert_execute_code_cell` | PASS | Output: `MCP_SPARK_OK 4.1.3 10`. |
| Frontend | `notebook_get_selected_cell` | PASS | Selected cell 0 reported successfully. |
| Frontend | Select next/previous cell | NOT EXPOSED | No tools for ordinary next/previous cell selection. |
| Frontend | `documentsearch_start` | PASS | Search for `MCP_STREAM_OK` accepted. |
| Frontend | `documentsearch_highlightNext` | PASS | Command completed successfully. |
| Frontend | `documentsearch_highlightPrevious` | PASS | Command completed successfully. |
| Frontend | `filebrowser_go_to_path` | PASS | Navigated to notebook’s root directory. |
| Frontend | `filebrowser_refresh` | PASS | Refresh completed successfully. |
| Frontend | `filebrowser_toggle_hidden_files` | PASS | Toggled twice, restoring original state. |
| Frontend | `application_toggle_left_area` | PASS | Toggled twice, restoring original state. |
| Frontend | `application_toggle_right_area` | PASS | Toggled twice, restoring original state. |
| Frontend | `application_toggle_presentation_mode` | PASS | Toggled twice, restoring original state. |
| Frontend | Open File/Edit/Help menus | NOT EXPOSED | No corresponding menu-opening tools. |
| Frontend | Theme restoration | NOT EXPOSED | No theme getter/restorer exposed; theme was not changed. |
| Run-all | `notebook_run_all_cells` | PASS | Returned `True`; readback showed execution counts 6–8. |
| Run-all | `read_cell` | PASS | Expected execute, stream, and Spark outputs persisted. |
| Kernel | `restart_notebook` | PASS | Kernel restarted successfully. |
| Kernel | `execute_code` after restart | PASS | Output: `MCP_RESTART_OK 42`. |
| Disconnect | `unuse_notebook` | PASS | Notebook disconnected and current notebook returned to `default`. |
| Disconnect | `list_notebooks` | PASS | Test notebook no longer appeared in the active registry. |
| Disconnect | `list_kernels` | PASS | Kernel remained `idle`, with one frontend connection. |
| Artifact | `list_files` | PASS | Saved notebook confirmed at root, size 2.9 KB. |

**Conclusion**

- Core MCP transport: **PASS** — all mandatory core tools succeeded; no JSON-RPC or SSE transport errors.
- Notebook CRUD/editing: **PASS**
- Code execution: **PASS**
- Streaming notifications: **PASS**
- Spark: **PASS**, version `4.1.3`
- JupyterLab frontend: **PASS for all exposed commands**
- Kernel lifecycle: **PASS** — restart and post-restart execution succeeded; kernel remained idle after disconnect because the frontend connection remained attached.
- Test notebook path: `jupyter-mcp-complete-test.ipynb`
- Failed call: `list_files(max_depth=4)` validation error; successfully recovered with `max_depth=3`.
- Unavailable operations: next-cell selection, previous-cell selection, File menu, Edit menu, Help menu, and theme query/restoration.
- Overall result: **PARTIAL PASS** — every mandatory core operation passed, but several requested optional frontend operations were not exposed.
