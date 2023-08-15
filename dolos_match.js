import { Dolos } from "@dodona/dolos-lib";

// Each of the two file paths is given by argument input
const files = process.argv.slice(2);

const dolos = new Dolos();
const report = await dolos.analyzePaths(files);

for (const pair of report.allPairs()) {
   for (const fragment of pair.buildFragments()) {
    const left = fragment.leftSelection;
    const right = fragment.rightSelection;
    console.log(`${pair.leftFile.path}:{${left.startRow},${left.startCol} -> ${left.endRow},${left.endCol}} matches with ${pair.rightFile.path}:{${right.startRow},${right.startCol} -> ${right.endRow},${right.endCol}}`);
 }
}