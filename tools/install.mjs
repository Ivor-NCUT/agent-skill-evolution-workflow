#!/usr/bin/env node
import { existsSync, lstatSync, mkdirSync, readdirSync, readlinkSync, symlinkSync, unlinkSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const target = path.resolve(process.env.SKILLS_HOME || path.join(process.env.CODEX_HOME || path.join(homedir(), ".codex"), "skills"));
const forceLinks = process.argv.includes("--force-links");
mkdirSync(target, { recursive: true });
for (const name of readdirSync(path.join(root, "skills"))) {
  const source = path.join(root, "skills", name);
  const link = path.join(target, name);
  if (existsSync(link)) {
    const stat = lstatSync(link);
    const same = stat.isSymbolicLink() && path.resolve(path.dirname(link), readlinkSync(link)) === source;
    if (same) { console.log(`ok ${name}`); continue; }
    if (!forceLinks || !stat.isSymbolicLink()) throw new Error(`${link} exists and is not the managed link`);
    unlinkSync(link);
  }
  symlinkSync(source, link, "dir");
  console.log(`installed ${name}`);
}
