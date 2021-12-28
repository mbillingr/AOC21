fn main() {
    let mut last = 0;
    let mut digits = vec![9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9];
    // 99959949929641
    loop {
        decrement(&mut digits);

        if digits[5] != last {
            println!("{:?}", digits);
            last = digits[5];
        }

        if check_alu(&digits) {
            println!("{:?}", digits);
            return;
        }
    }
}

type T = i64;

fn decrement(digits: &mut [i64]) {
    for i in (0..digits.len()).rev() {
        digits[i] -= 1;
        if digits[i] == 0 {
            digits[i] = 9;
        } else {
            return;
        }
    }
}

fn alu(input: &[i64]) -> i64 {
    let w1 = input[0];
    let w2 = input[1];
    let w3 = input[2];
    let w4 = input[3];
    let w5 = input[4];
    let w6 = input[5];
    let w7 = input[6];
    let w8 = input[7];
    let w9 = input[8];
    let w10 = input[9];
    let w11 = input[10];
    let w12 = input[11];
    let w13 = input[12];
    let w14 = input[13];

    let z = w1 * 26 + w2 + 6;
    let z = z * 26 + w3 + 4;
    let z = z * 26 + w4 + 2;

    let z = block_a(z, w5, w6, -7, 1);
    let z = block_a(z, w7, w8, 5, 6);
    assert!(z >= 26 * 26 * 26);
    let z = block_b(z, w9, 10, 4);
    assert!(z >= 26 * 26);
    let z = block_a(z, w10, w11, 4, 3);
    let z = block_b(z, w12, 4, 9);
    let z = block_b(z, w13, 1, 15);
    block_b(z, w14, 1, 5)
}

#[inline(always)]
fn block_a(z: i64, wa: i64, wb: i64, w_diff: i64, offset: i64) -> i64 {
    if wa - wb == w_diff {
        z
    } else {
        z * 26 + wb + offset
    }
}

#[inline(always)]
fn block_b(z: i64, w: i64, dx: i64, offset: i64) -> i64 {
    if z % 26 == w + dx {
        z / 26
    } else {
        (z / 26) * 26 + w + offset
    }
}

fn check_alu(input: &[i64]) -> bool {
    let w1 = input[0];
    let w2 = input[1];
    let w3 = input[2];
    let w4 = input[3];
    let w5 = input[4];
    let w6 = input[5];
    let w7 = input[6];
    let w8 = input[7];
    let w9 = input[8];
    let w10 = input[9];
    let w11 = input[10];
    let w12 = input[11];
    let w13 = input[12];
    let w14 = input[13];

    // I arrived at this solution by setting the result of alu() equal to zero,
    // and then repeated inlining, simplifying and eliminating branches that
    // could never be true...

    (w6 == w5 + 7)
        && (w7 == w8 + 5)
        && (w10 == w11 + 4)
        && (w4 == w9 + 8)
        && (w3 == w12)
        && (w2 + 5 == w13)
        && (w1 == w14 + 1)

    // From these rules, it follows that the largest possible number is
    // 94992994195998

    // And the smallest number is
    //

    // 1  2  3  4  5  6  7  8  9 10 11 12 13 14
    //[2, 1, 1, 9, 1, 8, 6, 1, 1, 5, 1, 1, 6, 1]
    //[9, 4, 9, 9, 2, 9, 9, 4, 1, 9, 5, 9, 9, 8]
}

fn modshift(z: T, n: T) -> T {
    z * 26
}

#[cfg(test)]
mod tests {
    use super::*;

    use rand;
    use rand::Rng;

    #[test]
    fn isok() {
        assert_eq!(alu(&[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), 394424504);
        assert_eq!(alu(&[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]), 2964603760);
        assert_eq!(alu(&[1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5]), 407276152);
        assert_eq!(alu(&[9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0]), 2951752107);
        assert_eq!(alu(&[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 73152097);
        assert_eq!(alu(&[0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0]), 2813621);
        assert_eq!(alu(&[0, 0, 0, 0, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0]), 2813621);
        assert_eq!(alu(&[0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 0, 0, 0]), 4165);

        // Part 1: 94992994195998
        assert_eq!(alu(&[9, 4, 9, 9, 2, 9, 9, 4, 1, 9, 5, 9, 9, 8]), 0);
        // Part 2: 21191861151161
        assert_eq!(alu(&[2, 1, 1, 9, 1, 8, 6, 1, 1, 5, 1, 1, 6, 1]), 0);
    }

    #[test]
    fn verify_assumptions() {
        let mut rng = rand::thread_rng();
        loop {
            let digits: Vec<_> = (0..14).map(|_| rng.gen_range(1..=9)).collect();
            if alu(&digits) == 0 {
                let x: Vec<_> = digits.into_iter().map(|d| d.to_string()).collect();
                panic!("{}", x.join(""))
            }
        }
    }
}
