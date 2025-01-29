//
// Created by xNosn on 2/19/2024.
//

#ifndef RAY_TRACER_VEC_H
#include <cmath>

class Vec {
private:

public:
    float x;
    float y;
    float z;

    explicit Vec(float x_ = 0, float y_ = 0, float z_ = 0) {
        x = x_;
        y = y_;
        z = z_;
    }

    Vec operator+(const Vec& other) const {
        return Vec(x + other.x, y + other.y, z + other.z);
    }

    Vec operator-(const Vec& other) const {
        return Vec(x - other.x, y - other.y, z - other.z);
    }

    Vec operator*(float scalar) const {
        return Vec(x * scalar, y * scalar, z * scalar);
    }
    Vec operator*(Vec v2) const {
        return Vec(x * v2.x, y * v2.y, z * v2.z);
    }

    Vec operator/(double t) const {
        return Vec(x * 1 / t, y * 1 / t, z * 1 / t);
    }

    Vec operator %(float min) const{
        return Vec(std::fmin(1,x), std::fmin(1,y), std::fmin(1,z));
    }

    Vec normalize() const {
        float length = std::sqrt(x * x + y * y + z * z);
        return Vec(x / length, y / length, z / length);
    }

    Vec cross(Vec v2) const {
        float xTmp = y * v2.z - z * v2.y;
        float yTmp = z * v2.x - this->x * v2.z;
        float zTmp = this->x * v2.y - this->y * v2.x;

        return Vec(xTmp,yTmp,zTmp);

    }

    float angle(Vec v2) const{
        Vec v1 = *this;
        float dot = v1.dot(v2);

        float magU = std::sqrt(v1.dot(v1));
        float magV = std::sqrt(v2.dot(v2));

        float cosineTheta = dot / (magU * magV);
        cosineTheta = std::fmax(-1.0f, std::fmin(1.0f, cosineTheta));

        float theta = std::acos(cosineTheta);
        return theta;

    }

    float dot(const Vec& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    float length() {
        return std::sqrt(x * x + y * y + z * z);
    }

};


#endif //RAY_TRACER_VEC_H
