# Santa 2025: Tree Packing Challenge

## Overview
The goal of this competition is to pack as many Christmas Trees as possible into the smallest axis-aligned bounding square. This is a geometry-based tiling and optimization challenge.

## Goal
Minimize the final score, which is determined by the size of the bounding box relative to the number of trees successfully placed.

## Evaluation
Submissions are evaluated on the efficiency of the packing:
$$Score = \frac{SideLength^2}{N}$$

Where:
- **SideLength:** The side length of the smallest axis-aligned bounding square that contains all placed trees.
- **N:** The total number of trees successfully packed.

### Submission Format
The submission file should be a CSV with a header and the following format:
```csv
id,x,y,deg
001_0,s0.0,s0.0,s20.411299
002_0,s0.0,s0.0,s20.411299
002_1,s-0.541068,s0.259317,s51.66348
```
*Note: Values must be strings prefixed with 's'.*

## Timeline
- **Start Date:** December 1, 2025
- **Final Submission Deadline:** December 31, 2025 (11:59 PM UTC)