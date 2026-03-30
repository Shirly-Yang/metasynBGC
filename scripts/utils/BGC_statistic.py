# -*- coding: utf-8 -*-

import os
from Bio import SeqIO
import pandas as pd
from multiprocessing import Pool, cpu_count


############################################
# USER SETTINGS
############################################

ROOT = "/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/GCF_select_fold/"
OUT_FILE = "antiSMASH_region_BGC_parallel.csv"

# ⭐ HPC强烈建议限制CPU
WORKERS = min(cpu_count()-1, 12)

# multiprocessing调度优化（非常重要）
CHUNKSIZE = 32


############################################
# STEP 1 — generator扫描GBK（无列表）
############################################

def find_gbk_files(root):

    for dirpath, dirnames, filenames in os.walk(root):

        # ⭐ 更严格的目录判断
        if "BGC_result" not in dirpath:
            continue

        for f in filenames:

            if "region" in f and f.endswith((".gbk", ".gbff")):
                yield os.path.join(dirpath, f)


############################################
# STEP 2 — 单文件解析
############################################

def parse_gbk(gbk_path):

    rows = []

    try:
        for record in SeqIO.parse(gbk_path, "genbank"):

            definition = record.description

            genome = None
            contig = None

            if ":" in definition:
                genome, contig = definition.split(":", 1)

            for feature in record.features:

                # ⭐ 只统计cand_cluster（发表口径）
                if feature.type != "cand_cluster":
                    continue

                q = feature.qualifiers

                start = int(feature.location.start)
                end = int(feature.location.end)

                row = {
                    "Genome": genome,
                    "Contig": contig,
                    "Definition": definition,
                    "BGC_type": q.get("product", [None])[0],
                    "Length_bp": end - start,
                    "Start": start,
                    "End": end,
                    "SMILES": q.get("SMILES", [None])[0],
                    "core_location": q.get("core_location", [None])[0],
                    "detection_rule": q.get("detection_rules", [None])[0],
                    "neighbourhood": q.get("neighbourhood", [None])[0],
                    "contig_edge": q.get("contig_edge", [None])[0],
                    
                    # 强烈推荐字段
                    "is_fragmented": q.get("contig_edge", ["False"])[0] == "True",

                    "candidate_cluster_number": q.get("candidate_cluster_number", [None])[0],
                    "tool": q.get("tool", [None])[0],
                    "gbk_file": gbk_path
                }

                rows.append(row)

    except Exception as e:
        print("FAILED:", gbk_path)
        print(e)

    return rows


############################################
# STEP 3 — 并行 + 边写入（恒定内存）
############################################

def main():

    print("Starting BGC scan...")
    print("Workers:", WORKERS)

    gbk_iter = find_gbk_files(ROOT)

    first_write = True
    total_clusters = 0
    total_files = 0

    with Pool(WORKERS) as pool:

        for result in pool.imap_unordered(parse_gbk, gbk_iter, chunksize=CHUNKSIZE):

            total_files += 1

            if not result:
                continue

            df_chunk = pd.DataFrame(result)

            df_chunk.to_csv(
                OUT_FILE,
                mode='w' if first_write else 'a',
                header=first_write,
                index=False
            )

            first_write = False
            total_clusters += len(df_chunk)

            # ⭐ 简单进度日志（比tqdm更HPC友好）
            if total_files % 500 == 0:
                print(f"Processed files: {total_files} | Total BGC: {total_clusters}")

    print("\nDONE.")
    print("Total GBK parsed:", total_files)
    print("Total BGC:", total_clusters)
    print("Saved to:", OUT_FILE)


############################################

if __name__ == "__main__":
    main()
