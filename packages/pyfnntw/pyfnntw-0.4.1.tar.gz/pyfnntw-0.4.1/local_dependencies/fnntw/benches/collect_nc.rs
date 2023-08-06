use fnntw::Tree;

use num_format::{Locale, ToFormattedString};
use std::time::Instant;

type T = f64;
const D: usize = 3;

fn collect_bench() {
    const RUNS: u128 = 100;

    let mut collect_time = 0;

    for _ in 0..RUNS {
        // Bench building tree
        for ndata in [5].map(|p| 10_usize.pow(p)) {
            let data: Vec<[T; D]> = (0..ndata)
                .map(|_| [(); D].map(|_| rand::random()))
                .collect();

            let time = Instant::now();
            let tree = Tree::new(&data, 32).unwrap();
            collect_time += time.elapsed().as_nanos();
            drop(tree)
        }
    }

    println!(
        "average collect time is {} nanos",
        (collect_time / RUNS).to_formatted_string(&Locale::en)
    );
}

fn par_collect_bench() {
    const RUNS: u128 = 100;

    let mut collect_time = 0;

    for _ in 0..RUNS {
        // Bench building tree
        for ndata in [5].map(|p| 10_usize.pow(p)) {
            let data: Vec<[T; D]> = (0..ndata)
                .map(|_| [(); D].map(|_| rand::random()))
                .collect();

            let time = Instant::now();
            let tree = Tree::new(&data, 32).unwrap();
            collect_time += time.elapsed().as_nanos();
            drop(tree)
        }
    }

    println!(
        "average collect time is {} nanos",
        (collect_time / RUNS).to_formatted_string(&Locale::en)
    );
}

fn main() {
    collect_bench();
    par_collect_bench();
}
