import * as fs from "fs";
import * as path from "path";
import * as vscode from "vscode";

export function findFlutterProjectRoot(startPath: string): string | undefined {
  let dir = path.resolve(startPath);
  const { root } = path.parse(dir);
  while (true) {
    if (fs.existsSync(path.join(dir, "pubspec.yaml"))) {
      return dir;
    }
    if (dir === root) {
      return undefined;
    }
    dir = path.dirname(dir);
  }
}

export function readDomainFolder(projectRoot: string): string {
  const cfg = path.join(projectRoot, "flutterator.yaml");
  if (fs.existsSync(cfg)) {
    const text = fs.readFileSync(cfg, "utf8");
    const m = text.match(/^\s*domain_folder:\s*["']?([^"'\n#]+)["']?\s*$/m);
    if (m) {
      return m[1].trim();
    }
  }
  return "domain";
}

/** Path relative to `lib/` for a folder under the project (e.g. features/components), or undefined. */
export function libRelativeFolder(projectRoot: string, folderFsPath: string): string | undefined {
  const lib = path.join(projectRoot, "lib");
  const abs = path.resolve(folderFsPath);
  const libAbs = path.resolve(lib);
  if (abs === libAbs) {
    return undefined;
  }
  const rel = path.relative(libAbs, abs);
  if (rel.startsWith("..") || rel === "") {
    return undefined;
  }
  return rel.split(path.sep).join("/");
}

export async function pickWorkspaceFlutterRoot(
  hintUri?: vscode.Uri
): Promise<{ projectRoot: string; contextLibFolder?: string } | undefined> {
  if (hintUri && hintUri.fsPath) {
    const stat = await fs.promises.stat(hintUri.fsPath).catch(() => undefined);
    if (stat?.isDirectory()) {
      const root = findFlutterProjectRoot(hintUri.fsPath);
      if (root) {
        const ctx = libRelativeFolder(root, hintUri.fsPath);
        return { projectRoot: root, contextLibFolder: ctx };
      }
    }
  }

  const folders = vscode.workspace.workspaceFolders;
  if (!folders?.length) {
    void vscode.window.showErrorMessage("Open a folder or workspace first.");
    return undefined;
  }
  if (folders.length === 1) {
    const root = findFlutterProjectRoot(folders[0].uri.fsPath);
    if (!root) {
      void vscode.window.showErrorMessage("No pubspec.yaml found in the workspace folder.");
      return undefined;
    }
    return { projectRoot: root };
  }

  const picked = await vscode.window.showWorkspaceFolderPick({
    placeHolder: "Select workspace folder containing the Flutter project",
  });
  if (!picked) {
    return undefined;
  }
  const root = findFlutterProjectRoot(picked.uri.fsPath);
  if (!root) {
    void vscode.window.showErrorMessage("No pubspec.yaml under the selected workspace folder.");
    return undefined;
  }
  return { projectRoot: root };
}

export function asUri(arg: unknown): vscode.Uri | undefined {
  if (!arg) {
    return undefined;
  }
  if (arg instanceof vscode.Uri) {
    return arg;
  }
  if (typeof arg === "string") {
    return vscode.Uri.file(arg);
  }
  if (typeof arg === "object" && arg !== null && "fsPath" in arg) {
    return vscode.Uri.file(String((arg as { fsPath: string }).fsPath));
  }
  return undefined;
}
