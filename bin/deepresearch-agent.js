#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const path = require("node:path");

const projectRoot = path.resolve(__dirname, "..");
const pythonCandidates = ["python3", "python"];

function runWithPython(pythonCmd) {
  return spawnSync(pythonCmd, ["cli.py"], {
    cwd: projectRoot,
    stdio: "inherit",
    env: process.env,
  });
}

for (const cmd of pythonCandidates) {
  const result = runWithPython(cmd);
  if (!result.error) {
    process.exit(result.status ?? 0);
  }
}

console.error(
  "Could not find a Python interpreter. Please install Python 3 and run again."
);
process.exit(1);
