const fs = require('node:fs')
const path = require('node:path')

async function run() {
  const [source, output, converterPath] = process.argv.slice(2)
  const importer = await require(path.resolve(converterPath))()
  const mesh = importer.ReadStepFile(fs.readFileSync(source), null)
  if (!mesh.success) throw Error('The STEP file did not produce a mesh')
  fs.writeFileSync(output, JSON.stringify(mesh))
}

run().catch(error => {
  console.error(error)
  process.exitCode = 1
})
