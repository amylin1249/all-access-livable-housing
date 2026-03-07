

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, help="number of elements to sample")
    parser.add_argument(
        "--quadtree", action="store_true", help="Use quadtree spatial index"
    )
    args = parser.parse_args()

    facilities = load_frs_csv(Path("data/il_frs.csv"))
    tracts = load_shapefiles(Path("data/il_tracts"))

    if args.sample >= len(facilities):
        print(f"Loaded {len(facilities)}, using all records")
    else:
        print(f"Loaded {len(facilities)}, sampling {args.sample}")

    facilities = facilities[: args.sample]

    if args.quadtree:
        spatial_join = quadtree_spatial_join
    else:
        spatial_join = basic_spatial_join

    start_time = time.time()
    results = spatial_join(facilities, tracts)
    elapsed = time.time() - start_time

    print(f"Found {len(results)} matches in {elapsed:.2f} seconds")

    with open("matches.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("frs_id", "tract_id"))
        writer.writerows(results)


if __name__ == "__main__":
    print("Hello from project-all-access-livable-housing!")
    main()
