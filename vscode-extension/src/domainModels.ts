import * as fs from "fs";
import * as path from "path";

export interface DomainModelPick {
  stem: string;
  label: string;
}

function isEntityDartFile(filePath: string): boolean {
  const name = path.basename(filePath);
  if (name.endsWith(".freezed.dart") || name.endsWith(".g.dart")) {
    return false;
  }
  if (name.startsWith("i_") || name.endsWith("_failure.dart")) {
    return false;
  }
  if (
    ["value_objects.dart", "value_validators.dart", "common_interfaces.dart"].includes(name)
  ) {
    return false;
  }
  try {
    const content = fs.readFileSync(filePath, "utf8");
    return /abstract class \w+\s+with\s+_\$/.test(content);
  } catch {
    return false;
  }
}

function classNameFromEntity(filePath: string): string | undefined {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    const m = content.match(/abstract class (\w+)\s+with/);
    return m ? m[1] : undefined;
  } catch {
    return undefined;
  }
}

/** Mirrors generators.helpers.feature.find_domain_models_with_class_names (flat domain root). */
export function listDomainModels(projectRoot: string, domainFolder: string): DomainModelPick[] {
  const lib = path.join(projectRoot, "lib");
  const domainPath = path.join(lib, ...domainFolder.split("/"));
  if (!fs.existsSync(domainPath)) {
    return [];
  }
  const picks: DomainModelPick[] = [];
  for (const ent of fs.readdirSync(domainPath, { withFileTypes: true })) {
    if (!ent.isDirectory()) {
      continue;
    }
    const modelDir = path.join(domainPath, ent.name, "model");
    if (!fs.existsSync(modelDir) || !fs.statSync(modelDir).isDirectory()) {
      continue;
    }
    for (const dart of fs.readdirSync(modelDir)) {
      if (!dart.endsWith(".dart")) {
        continue;
      }
      const fp = path.join(modelDir, dart);
      if (!isEntityDartFile(fp)) {
        continue;
      }
      const stem = path.basename(dart, ".dart");
      const cls = classNameFromEntity(fp) ?? stem;
      picks.push({ stem, label: `${cls} (${stem})` });
    }
  }
  picks.sort((a, b) => a.stem.localeCompare(b.stem));
  return picks;
}
