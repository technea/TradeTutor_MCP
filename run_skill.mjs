import { resolve } from 'path';
import { pathToFileURL } from 'url';

const [skillName, cmd, paramsStr] = process.argv.slice(2);

if (!skillName || !cmd) {
  console.error("Usage: node run_skill.mjs <skill-folder-name> <command> '<json-params>'");
  process.exit(1);
}

const cliPath = resolve(`.agents/skills/${skillName}/scripts/cli.mjs`);
const cliUrl = pathToFileURL(cliPath).href;

let cliModule;
try {
  cliModule = await import(cliUrl);
} catch (err) {
  console.error(`Failed to load skill '${skillName}' from ${cliPath}:`);
  console.error(err.message);
  process.exit(1);
}

const { COMMANDS, call } = cliModule;

if (!COMMANDS || !call) {
  console.error(`The skill module at ${cliPath} does not export 'COMMANDS' and 'call'.`);
  process.exit(1);
}

const builder = COMMANDS[cmd];
if (!builder) {
  console.error(`Unknown command: ${cmd}`);
  console.error(`Available commands: ${Object.keys(COMMANDS).join(', ')}`);
  process.exit(1);
}

let params = {};
if (paramsStr) {
  try {
    params = JSON.parse(paramsStr);
  } catch (err) {
    try {
      // Fallback for PowerShell stripping quotes (e.g., {chainId:56})
      params = (new Function(`return ${paramsStr}`))();
    } catch (err2) {
      console.error(`Invalid JSON params: ${err.message}`);
      process.exit(1);
    }
  }
}

try {
  const result = await call(builder(params));
  console.log(JSON.stringify(result, null, 2));
} catch (err) {
  console.error(err.message);
  if (err.body) {
    console.error(JSON.stringify(err.body, null, 2));
  }
  process.exit(err.exitCode || 1);
}
