#include "scene.h"

// All of the sdf are based on Inigo Quilez work 
// https://iquilezles.org/articles/distfunctions/
// which is licensed under the MIT license

plan::plan(const gbl::vec3& normal, double elevation):
  n(normal), height(elevation){}
  double plan::sdf(const gbl::vec3& p) const
{
  return dot(p,n) + height;
}

sphere::sphere(const gbl::vec3& center, double radius):
  c(center), r(radius){}
  double sphere::sdf(const gbl::vec3& p) const
{
  return gbl::norm(c-p)-r;
}

cylinder::cylinder(const gbl::vec3& a, const gbl::vec3& b, double r) :
  p0(a), p1(b), radius(r){}
  double cylinder::sdf(const gbl::vec3& p) const
{
  gbl::vec3 pa(p - p0), ba(p1 - p0);
  double h = clamp( gbl::dot(pa,ba)/gbl::dot(ba,ba), 0.0, 1.0 );
  return norm( pa - ba*h ) - radius;
}

opSub::opSub(std::shared_ptr<sdfable> to_keep, std::shared_ptr<sdfable> to_sub) :
  h_to_keep(to_keep), h_to_sub(to_sub) {}
  double opSub::sdf(const gbl::vec3& p) const
{
  return std::max(h_to_keep->sdf(p),-h_to_sub->sdf(p));
}

opInv::opInv(std::shared_ptr<sdfable> to_inv) :
  h(to_inv) {}
  double opInv::sdf(const gbl::vec3& p) const
{
  return -h->sdf(p);
}

opUnion::opUnion(std::shared_ptr<sdfable> h1, std::shared_ptr<sdfable> h2) :
  h_1(h1), h_2(h2){}
  double opUnion::sdf(const gbl::vec3& p) const
{
  return std::min(h_1->sdf(p), h_2->sdf(p));
}

opDisplace::opDisplace(std::shared_ptr<sdfable> to_disp, std::function<double(const gbl::vec3&)> disp_func):
  h(to_disp), f(disp_func){}
double opDisplace::sdf(const gbl::vec3& p) const
{
  double d1 = h->sdf(p);
  double d2 = f(p);
  return d1+d2;
}

opScale::opScale(std::shared_ptr<sdfable> to_scale, double scale):
  h(to_scale), s(scale){}
double opScale::sdf(const gbl::vec3& p) const
{
  return h->sdf(p/s)*s;
}


opTranslate::opTranslate(std::shared_ptr<sdfable> to_translate,
 const gbl::vec3& translation):
  h(to_translate), t(translation){}
double opTranslate::sdf(const gbl::vec3& p) const
{
  return h->sdf(p-t);
}