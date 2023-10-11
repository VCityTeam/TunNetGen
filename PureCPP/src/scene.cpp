#include "scene.h"

// All of the sdf are based on Inigo Quilez work 
// https://iquilezles.org/articles/distfunctions/
// which is licensed under the MIT license

plan::plan(const gbl::vec3f& normal, float elevation):
  n(normal), height(elevation){}
  float plan::sdf(const gbl::vec3f& p) const
{
  return dot(p,n) + height;
}

sphere::sphere(const gbl::vec3f& center, float radius):
  c(center), r(radius){}
  float sphere::sdf(const gbl::vec3f& p) const
{
  return gbl::norm(c-p)-r;
}

cylinder::cylinder(const gbl::vec3f& a, const gbl::vec3f& b, float r) :
  p0(a), p1(b), radius(r){}
  float cylinder::sdf(const gbl::vec3f& p) const
{
  gbl::vec3f pa(p - p0), ba(p1 - p0);
  float h = clamp( gbl::dot(pa,ba)/gbl::dot(ba,ba), 0.0, 1.0 );
  return norm( pa - ba*h ) - radius;
}

opSub::opSub(std::shared_ptr<sdfable> to_keep, std::shared_ptr<sdfable> to_sub) :
  h_to_keep(to_keep), h_to_sub(to_sub) {}
  float opSub::sdf(const gbl::vec3f& p) const
{
  return std::max(h_to_keep->sdf(p),-h_to_sub->sdf(p));
}

opInv::opInv(std::shared_ptr<sdfable> to_inv) :
  h(to_inv) {}
  float opInv::sdf(const gbl::vec3f& p) const
{
  return -h->sdf(p);
}

opUnion::opUnion(std::shared_ptr<sdfable> h1, std::shared_ptr<sdfable> h2) :
  h_1(h1), h_2(h2){}
  float opUnion::sdf(const gbl::vec3f& p) const
{
  return std::min(h_1->sdf(p), h_2->sdf(p));
}

opDisplace::opDisplace(std::shared_ptr<sdfable> to_disp, std::function<float(const gbl::vec3f&)> disp_func):
  h(to_disp), f(disp_func){}
  float opDisplace::sdf(const gbl::vec3f& p) const
{
  float d1 = h->sdf(p);
  float d2 = f(p);
  return d1+d2;
}
