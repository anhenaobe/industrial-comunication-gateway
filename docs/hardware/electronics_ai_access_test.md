# Electronics AI — bounded Altium access smoke test

Date: 2026-11-06. **CURRENT RESULT: PASS** after the user opened Altium and requested a rerun. Native read, write, save, close, reopen and property readback succeeded. The separate file-library allowlist remains pending manual configuration. Initial failed-test observations below are retained as history; see the rerun section for current evidence.

## Environment and discovery

- Electronics AI 1.0.1 is registered and responsive through `mcp__mcp_electronics_ai__suite_status`, `mcp__mcp_electronics_ai__suite_catalog`, and `mcp__mcp_electronics_ai__suite_invoke`.
- Inspected the installed [setup skill](C:/Users/justa/.codex/plugins/cache/electronics-ai/mcp-electronics-ai/1.0.1/skills/electronics-ai-setup/SKILL.md) and `docs/PLUGIN_PACKAGE.md` before diagnostics. No setup, installation, update, download or configuration change was performed.
- `suite_status({})` returned enabled EDA and library backends, minimal toolset, and `native_editor_probed: false`. Catalog discovery subsequently succeeded without backend errors.
- Installed executable: `C:\Program Files\Altium\AD26\X2.EXE`, file/product version **26.9.1.10**, read from Windows file metadata. This is not a version read from a live Altium instance.
- OS process query found no running `X2` process. The native plugin query independently reported that Altium Designer is not running.
- The setup skill's `py -3.12 .../scripts/plugin_runtime.py doctor` diagnostic could not start because `py` is not recognized in this shell. No installation was attempted. This does not establish that Python itself is missing: the MCP server and catalog are already responsive.

## Exact tests and observations

All catalog requests used `with_schema: true`; invoked tool arguments followed the returned schemas.

| Operation | Arguments / observation | Result |
|---|---|---|
| `suite_status` | `{}`; server Electronics AI, enabled backends | MCP response succeeded; no native proof |
| `suite_catalog` | backend `eda`, query `app_context` | Schema for `eda__app_context` discovered |
| `suite_invoke` → `eda__app_context` | `{}` | `bridge_answering: false`, `active_document: {}`, `open_document_count: 0` |
| Same native context result | warning: `Altium Designer is not running`; `native_session_id: null`; `compiled_project_path: null` | Native read failed |
| Same native context result | `script_version_match: false`, `running_script_version: null`, deployed version `2026.11.04.electronics-ai-p3`; `unsaved_detection_complete: false` | No running-script or unsaved-state verification; false match is not proof of a stale script |
| `suite_catalog` | backend `eda`, query `document`, limit 100 | 81 advertised tools; creation, read, placement and save operations exposed |
| `suite_catalog` | backend `libraries`, query `list_components`, then full library catalog, limit 100 | 34 file-library operations exposed |
| `suite_invoke` → `libraries__list_components` | `filepath: C:\dev\7mo\design\industrial-linux-gateway\hardware\academic_rev1\libraries\Professor_shared.SchLib`, `include_metadata: true`, `limit: 3` | Rejected: `Path is outside configured allowed_paths` |

The native context's expected script project was:

`C:\Users\justa\AppData\Local\ElectronicsAI\scripts\eda-7edd5178d4b869e7\ElectronicsAI-EDA.PrjScr`

The returned native runtime/workspace paths were `C:\Users\justa\AppData\Local\ElectronicsAI` and its `workspace` subdirectory. No native launch, workspace switch, marker deletion or retry was attempted. No active project or real open document information could be obtained; the empty context is not a verified inventory of a running editor.

## Advertised capabilities versus tested capabilities

Native operations discovered include `eda__app_create_document`, `eda__app_get_active_document`, `eda__app_list_documents`, `eda__obj_query`, `eda__sch_place_components`, `eda__app_save_all`, `eda__proj_get_focused`, `eda__proj_list_open`, `eda__lib_get_components`, `eda__lib_get_footprints`, `eda__lib_copy_component` and `eda__lib_reload_library`. Their presence proves discoverability only. None was used to create, change or save a design.

The 34 file-library operations include readers (`libraries__read_schlib`, `libraries__read_pcblib`, `libraries__get_component`), validation (`libraries__validate_library`), footprint-link management (`libraries__manage_schlib_footprints`), copying/merging, and writers (`libraries__write_schlib`, `libraries__write_pcblib`, `libraries__write_libpkg`). These use the plugin's `original_python_ole` file backend, separately from the live Altium bridge. File access to the permitted professor source was blocked by the plugin's own path policy. No library content was returned or modified.

## Write, save and reopen gate

- **Native read:** FAIL — editor not running, bridge not answering.
- **Controlled write:** NOT ATTEMPTED, because the required read gate failed.
- **Native save:** NOT ATTEMPTED.
- **Reopen and persisted-object verification:** NOT ATTEMPTED.
- **Scratch files:** none created. Proposed future location: `C:\dev\Electronics_AI_Smoke_Test`, outside the gateway repository and professor library.
- No tool accepted a native write request. No native file or resistor/capacitor placement is claimed as evidence.

## Preservation

Located the original `shared_lib (1).IntLib` in the repository root. SHA-256 during this test: `91594ede8aadf6449fff5b44b7443deafeb73cfaf0bc1eb1ff434d8ac1fb6159`, matching the previous recorded hash. It was not extracted or edited.

Only this new report was written. Existing engineering reports, CAD libraries, gateway design files, requirements and firmware were not edited. Git status was checked before and after; pre-existing changes remain. No commit or push was performed.

## Required user actions and readiness

1. **USER ACTION REQUIRED:** Open the installed Altium Designer and leave it ready, with any modal dialog closed. Then request a rerun of this bounded test. Do not start a second native bridge instance. If the next read identifies a bridge-start requirement, follow that specific diagnostic rather than guessing script startup steps now.
2. For subsequent professor-library reads, authorize `C:\dev\7mo\design\industrial-linux-gateway\hardware\academic_rev1\libraries` in Electronics AI's configured library `allowed_paths` using its official configuration workflow. The original IntLib must remain untouched. No policy bypass or automatic configuration change was attempted here.
3. The `py` launcher diagnostic is unavailable. No Python installation is requested on this evidence alone; if the official diagnostic is needed, provide the path to an existing Python 3.12 interpreter.

**Initial assessment (superseded by rerun below): NOT READY.** The initial catalog response and executable metadata alone did not satisfy PASS.

## Rerun after Altium was opened — PASS

User explicitly confirmed that Altium was running without blocking dialogs and authorized the same isolated test. The setup skill and native edit safeguards were read again. No additional bridge instance was launched. All schemas used were discovered through `suite_catalog` in this session or the immediately preceding bounded test.

### Native read evidence

- `suite_status({})`: EDA `running: true`, `startup_status: ready`, 457 advertised EDA tools, no failure diagnostic. Status alone still does not probe the editor.
- `suite_invoke(name="eda__app_context", arguments={})`: **`bridge_answering: true`**, `script_version_match: true`, `script_hash_match: true`, no warnings. Running/deployed script version both `2026.11.04.electronics-ai-p3`.
- Native session ID: `20261106112756226-407893046`. Compiled/expected script project paths matched the path recorded above.
- Actual initial active document: `Home page.Engagement`, kind `Engagement`; 21 documents reported. Unsaved list empty but detection incomplete, so no global save was authorized or used.
- `eda__app_get_version({})`: **Altium Designer 26.9.1.10**, this time read through the live native plugin.
- `eda__proj_get_focused({})`: `buck_boost_pasives.LibPkg`, path `C:\dev\7mo\design\electronic-design-dc-dc\entregable\buck_boost_pasives.LibPkg`, 2 members. This existing project was not edited or used as the test target.

### Isolated write, save and reopen evidence

Scratch directory: **`C:\dev\Electronics_AI_Smoke_Test`**, outside the gateway repository. Retained as evidence.

1. `eda__app_create_document`: `kind: SCH`, `file_path: C:\dev\Electronics_AI_Smoke_Test\Access_Test.SchDoc`, **`add_to_project: false`**. Returned success, `saved: true`, `added_to_project: false`.
2. `eda__app_set_active_document` targeted that exact path. `eda__app_get_active_document` confirmed the scratch path and kind `SCH` before placement.
3. `eda__sch_place_components` with explicit `document_path` placed the two existing symbols below in one call; result **placed 2, failed 0, total 2**. Source was the existing editable `Professor_shared.SchLib`, read through Altium's native placement operation. No extraction or source editing occurred. This tests placement, not electrical qualification or pin-to-pad mapping.
4. `eda__obj_query` with type `eSchComponent`, properties `Designator.Text,Comment.Text,LibReference`, scope `doc:C:\dev\Electronics_AI_Smoke_Test\Access_Test.SchDoc` returned the two objects below, with zero unknown, failed or unreadable properties.
5. `eda__app_click_menu` → `File|Save`, `may_steal_focus: true`, with explicit scratch `checkpoint_files`, returned `ok: true`. **Save All was not used.** Disk inspection then found a 15,360-byte native `.SchDoc`.
6. `eda__app_click_menu` → `File|Close`, same explicit checkpoint target, returned `ok: true`. Native active-document read changed to `Home page.Engagement`, confirming the scratch document ceased to be active.
7. `eda__obj_run_process` used the documented `WorkspaceManager:OpenObject` process with `ObjectKind=Document|FileName=C:\dev\Electronics_AI_Smoke_Test\Access_Test.SchDoc` and explicit scratch checkpoint target. This operation correctly reported dispatch only. Actual reopening was separately confirmed by `eda__app_get_active_document`, returning the scratch path and `SCH` kind.
8. Repeated scoped `eda__obj_query` after reopening returned **exactly the same two objects and all three properties**; zero property diagnostics. This supplies persisted native readback evidence rather than relying on dispatch or save acknowledgments.

| Designator | Persisted comment/value | Persisted library reference | Placement in mils |
|---|---|---|---|
| R_SMOKE | 10k 1/10W | Res_10k_0603_1/10W | 1000,1000 |
| C_SMOKE | 0.1uF 50V | Cap_0.1uF_0603_50V | 2000,1000 |

Values/comments were inherited from existing symbols; recognizable designators were assigned during placement. The smoke test does not approve these parts for the gateway. The scratch sheet remains open after successful readback. No connections were drawn.

### Exact allowed_paths diagnosis and manual procedure

Read-only inspection of the actual backend template identifies this configuration file:

**`C:\Users\justa\.codex\plugins\data\mcp-electronics-ai\libraries.json`**

Its current setting is:

```json
{
  "allowed_paths": [
    "C:\\Users\\justa\\.codex\\plugins\\data\\mcp-electronics-ai\\cloud-libraries"
  ]
}
```

Thus the project library source directory is not authorized for the **file-library backend**. Native Altium placement succeeded through a separate backend; it does not demonstrate that the file-reader restriction has changed. The rejected file-reader call was not retried because configuration is unchanged.

Supported setup documentation: installed `docs/PLUGIN_PACKAGE.md`, “Configure the private runtime”, documents `plugin_runtime.py bootstrap --altium-exe ... --library-dir ...`; repeated `--library-dir` adds existing intended library roots. Source `scripts/plugin_runtime.py`, `bootstrap` implementation, confirms that this merges existing `allowed_paths`, backs up `libraries.json`, and writes that file. **Bootstrap also creates a new runtime and installs dependencies**, so it is outside this task's no-install constraint and was not run or recommended as a configuration-only command. The installed `docs/review/STORAGE_VARIANTS_2026-10-08.md`, “Dependencies”, also explicitly permits adding the intended directory to the library connector allowlist.

Minimum manual configuration without installation:

1. End the bounded test first and disconnect the Electronics AI MCP connection before editing its settings. Do not launch another bridge instance or change runtime/workspace identity.
2. Make a local backup of `libraries.json`, for example `libraries.json.before-project-path.bak`; preserve any existing settings.
3. In **that file only**, append this absolute directory string to `allowed_paths`, preserving the current cloud-cache entry:

```json
"C:\\dev\\7mo\\design\\industrial-linux-gateway\\hardware\\academic_rev1\\libraries"
```

4. Save valid JSON and reconnect Electronics AI (restart Codex only if the host offers no connection reload). The in-process library backend must reload configuration.
5. Rerun the read-only `libraries__list_components` call above against `Professor_shared.SchLib`. A successful native placement is not a substitute for this file-backend verification.

Do **not** edit `backend-template.json`, its integrity digest in `state.json`, plugin cache files, security code, or environment variables. Do not add a drive root or disable path checks. The backend template already points at the correct `libraries.json`; the problem is its intentionally narrow allowlist. No configuration or backup was created by this test; the steps above are for the user.

### Current readiness and limits

**Native smoke test: PASS.** Read, isolated placement, save, close/reopen, and persisted property readback are now demonstrated. No compiler, ERC, DRC, PCB routing, footprint geometry, pin-to-pad verification or IntLib compilation was performed. Two scratch placements are not two homologated gateway components.

**File-library preparation: pending allowlist change and reader retest.** The 34 previously discovered file-library operations remain advertised but project-library file access is not yet verified. After the user applies the narrow configuration change, library preparation can be separately authorized. This task stops at the smoke test.

Only this report and the external scratch workspace were intentionally written. No original professor library, gateway CAD file, previous engineering report, firmware or requirements document was edited. Native operation safeguards may retain local recovery checkpoints. No installs, downloads, configuration edits, commits or pushes were performed.
