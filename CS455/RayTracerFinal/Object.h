//
// Created by xNosn on 2/19/2024.
//

#ifndef RAY_TRACER_OBJECT_H
#define RAY_TRACER_OBJECT_H
#include <cmath>
#include <utility>
#include <vector>
#include "Ray.h"

class Light {
public:
    Vec direction;
    float intensity;
    Vec ambientColor;
    Vec directColor;

    Light(Vec direction_, float intensity_, Vec ambientColor_, Vec directColor_) : direction(direction_.normalize()), intensity(intensity_), ambientColor(ambientColor_),
                                                                                   directColor(directColor_) {}
};


class Material {
public:
    Vec objectColor;
    Vec specColor;
    float Kd; //diffuse coefficient
    float Ks; //specular coefficient
    float Ka;  //ambient coefficient
    float Kgls; //Glossiness coefficient
    float refl = 0;
    bool inShadow = false;

    Material(Vec objectColor_, Vec specColor_, float Kd_, float Ks_, float Ka_, float Kgls_) : objectColor(objectColor_),
                                                                                               specColor(specColor_), Kd(Kd_),
                                                                                               Ks(Ks_), Ka(Ka_), Kgls(Kgls_){}

    Vec phongIllumination(Vec point, Vec normal, Vec viewDir, Light light, bool inShadow_) const{
        Vec lightDirection = light.direction.normalize();
        Vec ambient = light.ambientColor * objectColor * Ka;
        if (inShadow_){
            return ambient;
        }
        Vec diffuse = (light.directColor * objectColor * Kd * std::max(0.0f,(normal.dot(lightDirection))));
        diffuse.x = std::max(0.0f,diffuse.x);
        diffuse.y = std::max(0.0f, diffuse.y);
        diffuse.z = std::max(0.0f, diffuse.z);
        Vec R = normal * std::max(0.0f,(lightDirection.dot(normal)) * 2) - lightDirection; //make sure this is ok.
        Vec specular = (light.directColor * specColor * Ks) * std::max(0.0f,(std::pow( viewDir.dot(R.normalize()), Kgls)));
        Vec color = ambient + diffuse + specular;
        color.x = std::max(0.0f,color.x);
        color.y = std::max(0.0f,color.y);
        color.z = std::max(0.0f,color.z);

        return color%1;
    }


};

class Object {
public:
    Material material;

    explicit Object(Material material_) : material(material_) {}

    virtual float intersect(Ray ray) const = 0;

    Material getMaterial() const{
        return material;
    }


};

class Polygon : public Object{
public:
    std::vector<Vec> vertices;

    Polygon(std::vector<Vec> &vertices_, Material material_) : Object(material_), vertices(std::move(vertices_)){
        Normalize();
    }

    float intersect(Ray ray) const override{
        float direction = normal.dot(ray.direction);
        float d = -vertices[0].x * normal.x - vertices[0].y * normal.y - vertices[0].z * normal.z;
        float vo = -(normal.dot(ray.origin) + d);
        float t = vo/direction;

        if(t <= 0){
            return 0;
        }
        Vec P = ray.origin + ray.direction*t;

        Vec e0 = vertices[1] - vertices[0];
        Vec e1 = vertices[2] - vertices[1];
        Vec e2 = vertices[0] - vertices[2];
        Vec c0 = P - vertices[0];
        Vec c1 = P - vertices[1];
        Vec c2 = P - vertices[2];

        if (normal.dot(e0.cross(c0)) > 0 &&
                normal.dot(e1.cross(c1)) > 0 &&
                normal.dot(e2.cross(c2)) > 0){
            return t;
        } else {
            return 0;
        }
    }

    Vec getNormal(){
        return normal;
    }


private:
    Vec normal;

    void Normalize(){
        Vec P0 = vertices[0];
        Vec P1 = vertices[1];
        Vec P2 = vertices[2];

        Vec v1 = P0 - P1;
        Vec v2 = P2 - P1;

        Vec normal_ = v2.cross(v1);
        this->normal = normal_;
    }



};

class Sphere : public Object {
public:
    Vec center;
    float radius;


    Sphere(const Vec &center_, float radius_, Material material_) : Object(material_),
                                                                                              center(center_),
                                                                                              radius(radius_) {}

    //Intersection test of my ray with sphere
    float intersect(Ray ray) const override {
        Vec origin = ray.origin;
        Vec direction = ray.direction;
        Vec oc = origin - center; //getting the origin - center vector
        float A = direction.dot(direction);
        float B = 2.0f * oc.dot(direction);
        float C = oc.dot(oc) - radius * radius;
        float discriminant = B * B - 4 * A * C;

        if (discriminant < 0) {
            return 0;
        }
        float sqrt_discriminant = std::sqrt(discriminant);
        float t0 = (-B - sqrt_discriminant) / (2.0f * A);
        if (t0 <= 0) {
           float t1 = (-B + sqrt_discriminant) / (2.0f * A);
           if (t1 <= 0){
               return 0;
           } else {
               return t1;
           }
        } else {
            return t0;
        }

    }

    Vec getCenter() const{
        return center;
    }

    float getRadius() const{
        return radius;
    }

};



#endif //RAY_TRACER_OBJECT_H
