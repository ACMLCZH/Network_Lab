#include <iostream>
#include <random>
#include <cmath>

using namespace std;

#define EPS 0.1
#define EPS_LINE 1e-3
#define EPS_RAD 0.1
#define MAX_TRY 100

#define square(x) ((x) * (x))

typedef pair<double, double> Point;

double randomf(double _min, double _max) {
    return ((double)(rand() % 65536) / 65536) * (_max - _min) + _min;
}

bool check_constraints(const Point & a, const Point & b, const Point & c) {
    if (fabs(a.first - b.first) < EPS || fabs(a.second - b.second) < EPS)
        return false;
    if (fabs(b.first - c.first) < EPS || fabs(b.second - c.second) < EPS)
        return false;
    if (fabs(c.first - a.first) < EPS || fabs(c.second - a.second) < EPS)
        return false;
    return true;
}

Point rotate(const Point & p, double theta) {
    double cos_theta = cos(theta);
    double sin_theta = sin(theta);
    return Point(
        p.first * cos_theta + p.second * sin_theta, 
        -p.first * sin_theta + p.second * cos_theta
    );
}

double random_rotate(Point & a, Point & b, Point & c) {
    if (check_constraints(a, b, c))
        return 0.0;
    int ntry = 0;
    while (ntry++ < MAX_TRY) {
        double theta = randomf(0.0, 2 * M_PI);
        Point new_a = rotate(a, theta);
        Point new_b = rotate(b, theta);
        Point new_c = rotate(c, theta);
        if (check_constraints(new_a, new_b, new_c)) {
            a = new_a;
            b = new_b;
            c = new_c;
            return theta;
        }
    }
    return NAN;
}

Point calc_pos_sub(Point a, Point b, Point c, double da, double db, double dc) {
    double div_ba = (b.first - a.first) / (b.second - a.second);
    double div_ca = (c.first - a.first) / (c.second - a.second);
    double long_1 = square(da) - square(db) - square(a.first) - square(a.second) + square(b.first) + square(b.second);
    double long_2 = square(da) - square(dc) - square(a.first) - square(a.second) + square(c.first) + square(c.second);
    double x = ((long_1 / (2 * (b.second - a.second))) - (long_2 / (2 * (c.second - a.second)))) / (div_ba - div_ca);
    double y = ((long_1 / (2 * (b.first - a.first))) - (long_2 / (2 * (c.first - a.first)))) / ((1 / div_ba) - (1 / div_ca));
    return Point(x, y);
}

Point calc_pos(Point a, Point b, Point c, double da, double db, double dc) {
    if (da < 0 || db < 0 || dc < 0) {
        cerr << "Error: Got negative distance" << endl;
        return Point(-1, -1);
    }
    double theta = random_rotate(a, b, c);
    if (theta == NAN) {
        cerr << "Error: Failed to rotate points" << endl;
        return Point(-1, -1);
    }
    double div_ba = (b.first - a.first) / (b.second - a.second);
    double div_ca = (c.first - a.first) / (c.second - a.second);
    if (fabs(div_ba - div_ca) < EPS_LINE || fabs((1 / div_ba) - (1 / div_ca)) < EPS_LINE) {
        cerr << "Error: Points on a same line" << endl;
        return Point(-1, -1);
    }
    Point p1 = calc_pos_sub(a, b, c, da, db, dc);
    Point p2 = calc_pos_sub(b, c, a, db, dc, da);
    Point p3 = calc_pos_sub(c, a, b, dc, da, db);
    double d12 = sqrt(square(p1.first - p2.first) + square(p1.second - p2.second));
    double d23 = sqrt(square(p2.first - p3.first) + square(p2.second - p3.second));
    double d31 = sqrt(square(p3.first - p1.first) + square(p3.second - p1.second));
    double x = (d23 * p1.first + d31 * p2.first + d12 * p3.first) / (d23 + d31 + d12);
    double y = (d23 * p1.second + d31 * p2.second + d12 * p3.second) / (d23 + d31 + d12);
    Point p(x, y);
    p = rotate(p, -theta);
    return p;
}

void test_calc_pos(int n) {
    random_device rd;
    mt19937 gen(rd());
    normal_distribution<> d(1.0, 0.05);
    for (int i = 1; i <= n; i++) {
        Point a(randomf(0.0, 3.0), randomf(0.0, 3.0));
        Point b(randomf(0.0, 3.0), randomf(0.0, 3.0));
        Point c(randomf(0.0, 3.0), randomf(0.0, 3.0));
        Point pos(randomf(-1.0, 4.0), randomf(-1.0, 4.0));
        double da = sqrt(square(a.first - pos.first) + square(a.second - pos.second));
        double db = sqrt(square(b.first - pos.first) + square(b.second - pos.second));
        double dc = sqrt(square(c.first - pos.first) + square(c.second - pos.second));
        double da_noise = da * d(gen);
        double db_noise = db * d(gen);
        double dc_noise = dc * d(gen);
        Point pred = calc_pos(a, b, c, da_noise, db_noise, dc_noise);
        if (fabs(pred.first - pos.first) >= 1e-2 || fabs(pred.second - pos.second) >= 1e-2) {
            printf(
                "Test #%d: A(%.3f, %.3f), B(%.3f, %.3f), C(%.3f, %.3f), d(%.3f, %.3f, %.3f), d_noise(%.3f, %.3f, %.3f), real(%.3f, %.3f), pred(%.3f, %.3f)\n", 
                i, a.first, a.second, b.first, b.second, c.first, c.second, da, db, dc, da_noise, db_noise, dc_noise, pos.first, pos.second, pred.first, pred.second
            );
            printf("\n");
        }
    }
}

int main() {
    random_device rd;
    srand(rd());
    test_calc_pos(20);
    return 0;
}