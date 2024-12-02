//
// Created by xNosn on 2/19/2024.
//

#ifndef RAY_TRACER_RAY_H
#define RAY_TRACER_RAY_H
#include "Vec.h"


class Ray {
public:
    Vec origin;
    Vec direction;

    explicit Ray(Vec origin_, Vec direction_) : origin(origin_), direction(direction_){
    }


};


#endif //RAY_TRACER_RAY_H
