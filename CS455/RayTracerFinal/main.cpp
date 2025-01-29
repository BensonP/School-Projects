#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>
#include <limits>
#include <memory>
#include "Ray.h"
#include "Object.h"


Vec intersect(Ray ray, const std::vector<std::shared_ptr<Object>>& objects, std::shared_ptr<Object> closestObject, Vec pixelCenter, Vec cameraPos, Light light, int depth);

Vec const backgroundColor(.8,.2,.2);

int main() {
    auto aspectRatio = 1;
    int width = 1000;


    int height = static_cast<int>(width / aspectRatio);
    height = (height < 1) ? 1 : height;
    std::vector<Vec> framebuffer(width * height);

    std::vector<std::shared_ptr<Object>> objects;


    Light light(Vec(0, 0, 1), 1.0f, Vec(0.1,0.1,0.1), Vec(1.0,1.0,1.0));

    Material whiteSphereMaterial(Vec(1.0,1.0,1.0), Vec(1.0,1.0,1.0), 0.9, 0.1f, 0.3f, 4.0f);
    std::shared_ptr<Sphere> whiteSphere = std::make_shared<Sphere>(Vec(-0.3, 0.0, -.15), .05, whiteSphereMaterial);

    Material redSphereMaterial(Vec(1.0,0.0,0.0), Vec(.5,1.0,.5), 0.8, 0.8f, 0.1f, 32.0f);
    std::shared_ptr<Sphere> redSphere = std::make_shared<Sphere>(Vec(.3, -.4, -0.1), .08, redSphereMaterial);
    redSphereMaterial.refl = 0.9;

    Material greenSphereMaterial(Vec(0.0,1.0,0.0), Vec(.5,1.0,.5), 0.7, 0.9f, 0.1f, 64.0f);
    std::shared_ptr<Sphere> greenSphere = std::make_shared<Sphere>(Vec(-.6, .5, 0.0), .3, greenSphereMaterial);
    greenSphereMaterial.refl = 0.9;

    Material blueTriangle2Material(Vec(0.0,0.0,1.0), Vec(1.0,1.0,1.0), 0.9, 0.9f, 0.1f, 32.0f);
    blueTriangle2Material.refl = 0.9;
    std::vector<Vec> blueTriangle2Verts {Vec(0.0, -.5, -1.4), Vec(.5, 0.0, -0.0),Vec(0.0, 0.5, -2.0)};
    std::shared_ptr<Polygon> blueTriangle2 = std::make_shared<Polygon>(blueTriangle2Verts,blueTriangle2Material );

    Material yellowTriangle2Material(Vec(.75,.75,0.75), Vec(1.0,1.0,1.0), 0.9, 0.5f, 0.1f, 4.0f);
    std::vector<Vec> yellowTriangle2Verts {Vec(0.0, 0.5, -1.4), Vec(-0.5, 0.0, -.0), Vec(0.0, -0.5, -2.0)};
    std::shared_ptr<Polygon> yellowTriangle2 = std::make_shared<Polygon>(yellowTriangle2Verts,yellowTriangle2Material );
    yellowTriangle2Material.refl = 0.9;


    objects.push_back(redSphere);
    objects.push_back(greenSphere);
    objects.push_back(whiteSphere);
    objects.push_back(blueTriangle2);
    objects.push_back(yellowTriangle2);


    Material material7(Vec(1,1,0), Vec(1,1,1), 0.9, 1.0f, .1f, 4.0f);//yellow triangle
    Material material2(Vec(0.75,0.75,0.75), Vec(1,1,1), 0.0, 0.6f, .1f, 10.0f); //ref sphere
    material2.refl = .9;
    std::shared_ptr<Sphere> refSphere2 = std::make_shared<Sphere>(Vec(0.1, -0.55, 0.25), .3, material2);
    //objects.push_back(refSphere2);
    std::shared_ptr<Sphere> refSphere = std::make_shared<Sphere>(Vec(0, 0.0, -.5), .25, material2);
    Material material4(Vec(0,0,1), Vec(1,1,1), .9f, 1.0, .1f, 4.0f); //blue triangle

    Vec p0(0.0,-0.7,-0.5);
    Vec p1(1.0,0.4,-1.0);
    Vec p2(0.0,-0.7,-1.5);
    std::vector<Vec> vertices{p0,p1,p2};
    std::shared_ptr<Polygon> blueTriangle = std::make_shared<Polygon>(vertices, material4); //blue triangle

    std::vector<Vec> vertices2 {Vec(0.0, -0.7, -0.5), Vec(0.0, -0.7, -1.5), Vec(-1.0, 0.4, -1.0)};

    std::shared_ptr<Polygon> yellowTriangle = std::make_shared<Polygon>(vertices2, material7); // yellow triangle

    //objects.push_back(blueTriangle);
    //objects.push_back(yellowTriangle);
    objects.push_back(refSphere);



    float focalLength = 1.5;
    float viewportHeight = 2.0;
    float viewPortWidth = viewportHeight * (static_cast<float>(width)/height);
    Vec cameraPos(0, 0, 1);

    Vec viewportU(viewPortWidth, 0,0);
    Vec viewPortV(0, -viewportHeight, 0);

    auto pixelDeltaU = viewportU / width;
    auto pixelDeltaV = viewPortV / height;

    auto viewportUpperLeft = cameraPos - Vec(0,0,focalLength) - viewportU/2 - viewPortV/2;
    auto pixel00_loc = viewportUpperLeft + Vec(.5,.5,.5) * (pixelDeltaU + pixelDeltaV);
    Vec viewDir(0, 0, -1);
    Vec up(0, 1, 0);
    float distance = 1;
    Vec origin(0,0,distance);

    float const DEPTH = 4;


    for (int y = 0; y < height; ++y){
        for (int x = 0; x < width; ++x) {
            auto pixelCenter = pixel00_loc + (pixelDeltaU * float(x)) + (pixelDeltaV * float(y));
            auto rayDirection = (pixelCenter - cameraPos).normalize();

            Ray ray(origin, rayDirection);

            std::shared_ptr<Object> closestObject = nullptr;
            Vec color = intersect(ray, objects, closestObject, pixelCenter, cameraPos, light, DEPTH);
            if (color.x != 10000 && color.y != 10000 && color.z != 10000) {
                framebuffer[y * width + x] = color;
            } else {
                framebuffer[y * width + x] = backgroundColor;
            }
        }
    }

    std::ofstream  file("imageTriangle3.ppm");

    file  << "P3\n" << width << " " << height << "\n255\n";
    for (const auto& color : framebuffer) {
        file << static_cast<int>(color.x * 255) << " " << static_cast<int>(color.y * 255) << " " << static_cast<int>(color.z * 255) << "\n";
    }
}

Vec intersect(Ray ray, const std::vector<std::shared_ptr<Object>>& objects, std::shared_ptr<Object> closestObject, Vec pixelCenter, Vec cameraPos, Light light, int depth){
    if (depth <= 0){
        return  Vec(0,0,0);
    }
    bool inShadow = false;
    float max = std::numeric_limits<float>::max();
    float t = std::numeric_limits<float>::max();
    for(const auto& obj: objects) {
        float tTmp = obj ->intersect(ray);
        if (tTmp < t && tTmp > pow(2,-16)) {
            t = tTmp;
            closestObject = obj;
        }
    }
    if (t != max && t > 0) {
        Vec intersectionPoint = (ray.origin + ray.direction * t);
        Vec viewDirection = cameraPos - intersectionPoint;
        Ray shadow(intersectionPoint,(light.direction).normalize());
        for (const auto& obj:objects){
            float shadowInt = obj ->intersect(shadow);
            if (std::abs(shadowInt) > pow(2, -16)) {
                inShadow = true;
                break;
            } else{
                inShadow = false;
            }
        }

        Vec reflectionColor(1,1,1);
        if (auto sphere = std::dynamic_pointer_cast<Sphere>(closestObject)) {
            // Intersection point belongs to a sphere
            Vec normal = ((intersectionPoint - sphere->getCenter())/sphere->getRadius()).normalize();
            Vec color = sphere->getMaterial().phongIllumination(cameraPos, normal.normalize(), viewDirection.normalize(), light,
                                                                inShadow);
            if (!closestObject->material.inShadow){
                Vec reflectDirection(ray.direction - normal*2*(ray.direction.dot(normal)));
                Ray reflect(intersectionPoint, reflectDirection);
                reflectionColor = intersect(reflect, objects, closestObject, pixelCenter, cameraPos, light, depth-1);
                if (reflectionColor.x != 10000 && reflectionColor.y != 10000 && reflectionColor.z != 10000) {
                    color = color * (1-closestObject->material.refl) + reflectionColor*closestObject->material.refl;
                } else {
                    return color * (1-closestObject->material.refl) + backgroundColor * closestObject->material.refl;
                }
            }
            return color;
        } else if (auto polygon = std::dynamic_pointer_cast<Polygon>(closestObject)) {
            // Intersection point belongs to a polygon
            Vec normal = polygon->getNormal();
            Vec color = polygon->getMaterial().phongIllumination(cameraPos,normal.normalize(),viewDirection.normalize(), light,
                                                                 inShadow);
            if (!closestObject->material.inShadow){
                Vec reflectDirection(ray.direction - normal*2*(ray.direction.dot(normal)));
                Ray reflect(intersectionPoint, reflectDirection.normalize());
                reflectionColor = intersect(reflect, objects, closestObject, pixelCenter, cameraPos, light, depth-1);
                if (reflectionColor.x != 10000 && reflectionColor.y != 10000 && reflectionColor.z != 10000) {
                    color = color * (1-closestObject->material.refl) + reflectionColor*closestObject->material.refl;
                } else {
                    return color * (1-closestObject->material.refl)+ backgroundColor * closestObject->material.refl;
                }
            }
            return color;
        }

    } else return Vec(10000,10000,10000);
}

