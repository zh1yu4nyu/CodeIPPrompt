import { Dolos } from "@dodona/dolos-lib";

// Each of the two file paths is given by argument input
const files = process.argv.slice(2);

const dolos = new Dolos();
const report = await dolos.analyzePaths(files);

for (const pair of report.allPairs()) {
 const similarity = pair.similarity;
 console.log(`Similarity: ${similarity}`);
}