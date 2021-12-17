def main():
    # Part 1: Head-First solution
    #   1. Energy preservation: the y-velocity after the step entering y==0 on the way down will be start_velocity - 1
    #   2. The maximum y-position will be start_velocity * (start_velocity+1) / 2
    # => Highest peak reached when velocity is equal to the lowest allowed position (minus 1 because of gravitational acceleration)

    vy0_max = -INPUT["y"][0] - 1
    y_peak = vy0_max * (vy0_max + 1) // 2
    print("Day 17, part 1:", y_peak)

    # Part 2: Brute force within limited range

    ymin, ymax = INPUT["y"]
    xmin, xmax = INPUT["x"]

    n_possible_velocities = 0
    for vx in range(xmax + 2):
        for vy in range(ymin, vy0_max + 1):
            if simulate(vx, vy, (xmin, xmax), (ymin, ymax)):
                n_possible_velocities += 1

    print("Day 17, part 2:", n_possible_velocities)


def simulate(vx, vy, xrange, yrange):
    x, y = 0, 0
    while x <= xrange[1] and y >= yrange[0]:
        if x >= xrange[0] and y <= yrange[1]:
            return True

        x += vx
        y += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1

        vy -= 1
    return False


if __name__ == "__main__":
    INPUT = {"x": (29, 73), "y": (-248, -194)}  # "target area: x=29..73, y=-248..-194"
    main()
