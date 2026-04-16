import { spawn } from "child_process";
import * as vscode from "vscode";

export function getExecutable(): string {
  const cfg = vscode.workspace.getConfiguration("flutterator");
  return (cfg.get<string>("executablePath") || "flutterator").trim() || "flutterator";
}

export function runFlutterator(
  args: string[],
  cwd: string,
  channel: vscode.OutputChannel
): Promise<number> {
  const exe = getExecutable();
  channel.appendLine(`$ ${quoteCmd(exe, args)}`);
  channel.show(true);

  return new Promise((resolve) => {
    const child = spawn(exe, args, {
      cwd,
      env: { ...process.env, NO_COLOR: "1", FORCE_COLOR: "0" },
      shell: false,
    });
    child.stdout?.on("data", (d: Buffer) => channel.append(d.toString()));
    child.stderr?.on("data", (d: Buffer) => channel.append(d.toString()));
    child.on("close", (code) => {
      channel.appendLine(`(exit ${code ?? "?"})`);
      resolve(code ?? 1);
    });
    child.on("error", (err) => {
      channel.appendLine(String(err));
      resolve(1);
    });
  });
}

function quoteCmd(exe: string, args: string[]): string {
  const q = (s: string) => (/\s/.test(s) ? JSON.stringify(s) : s);
  return [q(exe), ...args.map(q)].join(" ");
}
