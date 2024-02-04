#include <memory>
#include <vector>
#include <functional>
#include "vec.h"
#include "utils.h"


// based on https://iquilezles.org/articles/distfunctions/
// More information about the licence (from https://iquilezles.org)
// "Legal: Code in this website or in my Shadertoy account that implements an algorithm is under the MIT license.
// Code in this website or in my Shadertoy account that implements an artwork is considered to be the artwork, and is copyrighted.

struct sdfable
{
  virtual double sdf(const gbl::vec3& p) const = 0;
};

struct plan : sdfable
{
  gbl::vec3 n;
  double height;

  plan(const gbl::vec3& normal, double elevation);
  double sdf(const gbl::vec3& p) const;
};

struct sphere : sdfable
{
  gbl::vec3 c;
  double r;

  sphere(const gbl::vec3& center, double radius);
  double sdf(const gbl::vec3& p) const;
};

struct cylinder : sdfable
{
  gbl::vec3 p0, p1;
  double radius;

  cylinder(const gbl::vec3& a, const gbl::vec3& b, double r);
  double sdf(const gbl::vec3& p) const;
};

struct cappedCone : sdfable
{
  gbl::vec3 p0, p1;
  double radius_a, radius_b;

  cappedCone(const gbl::vec3& a, const gbl::vec3& b, double ra, double rb);
  double sdf(const gbl::vec3& p) const;
};

struct opSub : sdfable
{
  std::shared_ptr<sdfable> h_to_keep, h_to_sub;
  opSub(std::shared_ptr<sdfable> to_keep, std::shared_ptr<sdfable> to_sub);
  double sdf(const gbl::vec3& p) const;
};

struct opInv : sdfable
{
  std::shared_ptr<sdfable> h;
  opInv(std::shared_ptr<sdfable> to_inv);
  double sdf(const gbl::vec3& p) const;
};

struct opUnion : sdfable
{
  std::shared_ptr<sdfable> h_1, h_2;
  opUnion(std::shared_ptr<sdfable> h1, std::shared_ptr<sdfable> h2);
  double sdf(const gbl::vec3& p) const;
};

struct opDisplace : sdfable
{
  std::shared_ptr<sdfable> h;
  std::function<double(const gbl::vec3&)> f;
  opDisplace(std::shared_ptr<sdfable> to_disp, 
    std::function<double(const gbl::vec3&)> disp_func);
  double sdf(const gbl::vec3& p) const;
};

struct opScale : sdfable
{
  std::shared_ptr<sdfable> h;
  double s;
  opScale(std::shared_ptr<sdfable> to_scale, 
     double scale);
  double sdf(const gbl::vec3& p) const;
};

struct opTranslate : sdfable
{
  std::shared_ptr<sdfable> h;
  gbl::vec3 t;
  opTranslate(std::shared_ptr<sdfable> to_translate, 
     const gbl::vec3& translation);
  double sdf(const gbl::vec3& p) const;
};
