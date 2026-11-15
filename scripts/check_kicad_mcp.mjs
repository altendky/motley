#!/usr/bin/env node
// Exercise the installed transport and Python bridge without a desktop or CAD edits.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const toolRoot = execFileSync("mise", ["where", "http:kicad-mcp"], {
  encoding: "utf8",
}).trim();
const { version } = JSON.parse(readFileSync(join(toolRoot, "package.json"), "utf8"));
const lockPath = new URL(`../.mise/locks/http-kicad-mcp/${version}/requirements.txt`, import.meta.url);
const runtimeCheck = `
import importlib, importlib.metadata as metadata, pathlib, re, sys
lock = pathlib.Path(sys.argv[1]).read_text()
for name, expected in re.findall(r"^([\\w-]+)==([^\\s]+)", lock, re.MULTILINE):
    actual = metadata.version(name)
    if actual != expected:
        raise RuntimeError(f"{name}: expected {expected}, found {actual}")
private_site = pathlib.Path(sys.argv[2]).resolve()
for name in ("kipy", "skip", "sexpdata", "PIL", "pymupdf", "cairosvg", "colorlog",
             "pydantic", "requests", "dotenv", "urllib3", "idna", "charset_normalizer"):
    module = importlib.import_module(name)
    if not pathlib.Path(module.__file__).resolve().is_relative_to(private_site):
        raise RuntimeError(f"{name} did not load from the private locked packages")
import pcbnew
import pymupdf
document = pymupdf.open()
page = document.new_page()
pixels = page.get_pixmap()
if pixels.width <= 0 or pixels.height <= 0:
    raise RuntimeError("PDF renderer produced no pixels")
print("Locked Python packages and pcbnew", pcbnew.GetBuildVersion(), "verified.")
`;
process.stdout.write(execFileSync(join(toolRoot, "bin/kicad-mcp-python"), [
  "-c", runtimeCheck, fileURLToPath(lockPath),
  join(toolRoot, "python-deps/lib/python3.11/site-packages"),
], { encoding: "utf8" }));
const sdkRoot = join(toolRoot, "node_modules/@modelcontextprotocol/sdk/dist/esm/client");
const { Client } = await import(pathToFileURL(join(sdkRoot, "index.js")));
const { StdioClientTransport } = await import(pathToFileURL(join(sdkRoot, "stdio.js")));
const env = { ...process.env, KICAD_BACKEND: "swig" };
delete env.DISPLAY;
delete env.WAYLAND_DISPLAY;
const transport = new StdioClientTransport({ command: "kicad-mcp", env, stderr: "pipe" });
const client = new Client({ name: "motley-kicad-check", version: "1" });
let diagnostics = "";
transport.stderr?.on("data", chunk => {
  diagnostics = (diagnostics + chunk.toString()).slice(-4000);
});

try {
  await client.connect(transport, { timeout: 30_000 });
  const { tools } = await client.listTools({}, { timeout: 30_000 });
  if (!tools.some(tool => tool.name === "get_backend_state")) {
    throw new Error("Installed server does not expose get_backend_state");
  }
  const response = await client.callTool({ name: "get_backend_state", arguments: {} },
    undefined, { timeout: 30_000 });
  const text = response.content?.find(item => item.type === "text")?.text;
  const state = text ? JSON.parse(text) : null;
  if (response.isError || state?.success !== true || state.backend !== "swig"
      || state.realtime !== false) {
    throw new Error(`Headless SWIG bridge check failed: ${text ?? "no state returned"}`);
  }
  console.log(`KiCad MCP initialized; ${tools.length} tools exposed; headless SWIG bridge ready.`);
} catch (error) {
  console.error(error.message);
  if (diagnostics) console.error(diagnostics);
  process.exitCode = 1;
} finally {
  await client.close();
}
