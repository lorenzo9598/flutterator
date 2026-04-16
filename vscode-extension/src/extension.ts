import * as fs from "fs";
import * as path from "path";
import * as vscode from "vscode";
import { listDomainModels } from "./domainModels";
import { asUri, pickWorkspaceFlutterRoot, readDomainFolder } from "./flutterProject";
import { getExecutable, runFlutterator } from "./runFlutterator";

let out: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext): void {
  out = vscode.window.createOutputChannel("Flutterator");
  context.subscriptions.push(out);

  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.showOutput", () => out.show(true))
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.create", async (arg) => {
      await cmdCreate(asUri(arg));
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.addPage", async (arg) => {
      await cmdAddPage(asUri(arg));
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.addDomain", async (arg) => {
      await cmdAddDomain(asUri(arg));
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.addComponent", async (arg) => {
      await cmdAddComponent(asUri(arg));
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("flutterator.addEnum", async (arg) => {
      await cmdAddEnum(asUri(arg));
    })
  );
}

export function deactivate(): void {
  /* noop */
}

async function cmdCreate(hint?: vscode.Uri): Promise<void> {
  const parent = await pickCreateParentFolder(hint);
  if (!parent) {
    return;
  }
  const name = await vscode.window.showInputBox({
    title: "Flutterator: Create",
    prompt: "Project name (lowercase, letters, numbers, _ and -)",
    validateInput: (v) => {
      const t = v.trim();
      if (!t) {
        return "Required";
      }
      if (!t.replace(/_/g, "").replace(/-/g, "").match(/^[a-zA-Z0-9]+$/)) {
        return "Only letters, numbers, _ and -";
      }
      return undefined;
    },
  });
  if (!name) {
    return;
  }
  const loginPick = await vscode.window.showQuickPick(
    [
      { label: "Yes", value: true as const },
      { label: "No", value: false as const },
    ],
    { title: "Include login / authentication?", placeHolder: "No" }
  );
  if (loginPick === undefined) {
    return;
  }
  const args = ["create", "--name", name.trim()];
  if (loginPick.value) {
    args.push("--login");
  } else {
    args.push("--no-login");
  }
  const code = await runFlutterator(args, parent, out);
  if (code === 0) {
    void vscode.window.showInformationMessage(`Flutterator: project '${name.trim()}' created.`);
  } else {
    void vscode.window.showErrorMessage(`Flutterator create failed (exit ${code}). See Output.`);
  }
}

async function pickCreateParentFolder(hint?: vscode.Uri): Promise<string | undefined> {
  if (hint?.fsPath) {
    try {
      const st = await fs.promises.stat(hint.fsPath);
      if (st.isDirectory()) {
        return hint.fsPath;
      }
    } catch {
      /* not found */
    }
  }
  const folders = vscode.workspace.workspaceFolders;
  if (folders?.length === 1) {
    return folders[0].uri.fsPath;
  }
  const picked = await vscode.window.showWorkspaceFolderPick({
    placeHolder: "Folder where the new project directory will be created",
  });
  return picked?.uri.fsPath;
}

async function cmdAddPage(hint?: vscode.Uri): Promise<void> {
  const ctx = await pickWorkspaceFlutterRoot(hint);
  if (!ctx) {
    return;
  }
  const name = await vscode.window.showInputBox({
    title: "Flutterator: Add Page",
    prompt: "Page name (e.g. profile, settings)",
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!name) {
    return;
  }
  const code = await runFlutterator(
    ["add-page", "--name", name.trim(), "--project-path", ctx.projectRoot],
    ctx.projectRoot,
    out
  );
  await notify(code, "Page added.");
}

async function cmdAddDomain(hint?: vscode.Uri): Promise<void> {
  const ctx = await pickWorkspaceFlutterRoot(hint);
  if (!ctx) {
    return;
  }
  const name = await vscode.window.showInputBox({
    title: "Flutterator: Add Domain",
    prompt: "Entity name (e.g. todo, NoteItem)",
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!name) {
    return;
  }
  const fields = await vscode.window.showInputBox({
    title: "Fields (optional)",
    prompt: 'Comma-separated name:type, e.g. title:string,done:bool — leave empty for id-only entity',
    placeHolder: "title:string,done:bool",
  });
  if (fields === undefined) {
    return;
  }
  const domainFolder = await vscode.window.showInputBox({
    title: "Domain folder (optional)",
    prompt: "Path under lib/ (default from flutterator.yaml or domain)",
    placeHolder: readDomainFolder(ctx.projectRoot),
  });
  if (domainFolder === undefined) {
    return;
  }
  const args = ["add-domain", "--name", name.trim(), "--project-path", ctx.projectRoot];
  const f = fields.trim();
  if (f) {
    args.push("--fields", f);
  } else {
    args.push("--non-interactive");
  }
  const df = domainFolder.trim();
  if (df) {
    args.push("--folder", df);
  }
  const code = await runFlutterator(args, ctx.projectRoot, out);
  await notify(code, "Domain entity added.");
}

async function cmdAddComponent(hint?: vscode.Uri): Promise<void> {
  const ctx = await pickWorkspaceFlutterRoot(hint);
  if (!ctx) {
    return;
  }
  const name = await vscode.window.showInputBox({
    title: "Flutterator: Add Component",
    prompt: "Component name (snake_case, e.g. user_card)",
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!name) {
    return;
  }
  const typePick = await vscode.window.showQuickPick(
    [
      { label: "Single (load by id)", value: "single" as const },
      { label: "List (CRUD)", value: "list" as const },
      { label: "Form", value: "form" as const },
    ],
    { title: "Component type", placeHolder: "single" }
  );
  if (!typePick) {
    return;
  }
  const defaultFolder =
    ctx.contextLibFolder || inferDefaultComponentFolder(ctx.projectRoot) || "features/components";
  const folder = await vscode.window.showInputBox({
    title: "Folder under lib/",
    prompt: "Target folder (relative to lib/)",
    value: defaultFolder,
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!folder) {
    return;
  }
  const domainFolder = readDomainFolder(ctx.projectRoot);
  const models = listDomainModels(ctx.projectRoot, domainFolder);
  const noneItem: vscode.QuickPickItem & { stem?: string } = {
    label: "$(circle-slash) No domain model",
    description: "Component without entity",
    stem: "none",
  };
  const modelItems: (vscode.QuickPickItem & { stem?: string })[] = models.map((m) => ({
    label: m.label,
    stem: m.stem,
  }));
  const domPick = await vscode.window.showQuickPick([noneItem, ...modelItems], {
    title: "Domain model",
    placeHolder: "Pick a model or none",
  });
  if (!domPick || !("stem" in domPick)) {
    return;
  }
  const domainStem = (domPick as { stem?: string }).stem;
  const domainArg = domainStem === "none" || domainStem === undefined ? "none" : domainStem;

  let extra: string[] = [];
  if (typePick.value === "form") {
    if (domainArg === "none") {
      const fields = await vscode.window.showInputBox({
        title: "Form fields",
        prompt: "name:type,name:type (required for form without domain model)",
        validateInput: (v) => (v.trim() ? undefined : "Required for form without model"),
      });
      if (!fields) {
        return;
      }
      extra.push("--fields", fields.trim());
    } else {
      const all = await vscode.window.showQuickPick(
        [
          { label: "Use all fields from the model", value: true as const },
          { label: "Skip (run will fail — use terminal for subset)", value: false as const },
        ],
        { title: "Form fields from domain model", placeHolder: "All fields" }
      );
      if (!all || !all.value) {
        void vscode.window.showWarningMessage(
          "Flutterator: subset selection is not supported headless yet; choose “All fields” or use the terminal."
        );
        return;
      }
      extra.push("--use-all-model-fields");
    }
  }

  const args = [
    "add-component",
    "--name",
    name.trim(),
    "--type",
    typePick.value,
    "--folder",
    folder.trim(),
    "--domain-model",
    domainArg,
    "--project-path",
    ctx.projectRoot,
    ...extra,
  ];
  const code = await runFlutterator(args, ctx.projectRoot, out);
  await notify(code, "Component added.");
}

function inferDefaultComponentFolder(projectRoot: string): string | undefined {
  const p = path.join(projectRoot, "flutterator.yaml");
  try {
    const text = fs.readFileSync(p, "utf8");
    const m = text.match(/^\s*component_folder:\s*["']?([^"'\n#]+)["']?\s*$/m);
    if (m) {
      return m[1].trim();
    }
  } catch {
    /* ignore */
  }
  const feat = path.join(projectRoot, "lib", "features", "components");
  if (fs.existsSync(feat)) {
    return "features/components";
  }
  return undefined;
}

async function cmdAddEnum(hint?: vscode.Uri): Promise<void> {
  const ctx = await pickWorkspaceFlutterRoot(hint);
  if (!ctx) {
    return;
  }
  const name = await vscode.window.showInputBox({
    title: "Flutterator: Add Enum",
    prompt: "Enum class name (PascalCase, e.g. EventStatus)",
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!name) {
    return;
  }
  const values = await vscode.window.showInputBox({
    title: "Enum values",
    prompt: "Comma-separated (e.g. pending,active,done)",
    validateInput: (v) => (v.trim() ? undefined : "Required"),
  });
  if (!values) {
    return;
  }
  const domainFolder = await vscode.window.showInputBox({
    title: "Domain folder (optional)",
    prompt: "Under lib/ (default from flutterator.yaml or domain)",
    placeHolder: readDomainFolder(ctx.projectRoot),
  });
  if (domainFolder === undefined) {
    return;
  }
  const overwrite = await vscode.window.showQuickPick(
    [
      { label: "No", value: false as const },
      { label: "Yes — pass --force if file exists", value: true as const },
    ],
    { title: "Overwrite existing enum file if present?", placeHolder: "No" }
  );
  if (overwrite === undefined) {
    return;
  }
  const force = overwrite.value === true;
  const args = [
    "add-enum",
    "--name",
    name.trim(),
    "--values",
    values.trim(),
    "--project-path",
    ctx.projectRoot,
  ];
  const df = domainFolder.trim();
  if (df) {
    args.push("--folder", df);
  }
  if (force) {
    args.push("--force");
  }
  const code = await runFlutterator(args, ctx.projectRoot, out);
  await notify(code, "Enum added.");
}

async function notify(code: number, okMsg: string): Promise<void> {
  if (code === 0) {
    void vscode.window.showInformationMessage(`Flutterator: ${okMsg}`);
  } else {
    void vscode.window.showErrorMessage(`Flutterator failed (exit ${code}). See Output “Flutterator”.`);
  }
}
