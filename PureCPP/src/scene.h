#include <memory>
#include <vector>
#include <functional>
#include "vec.h"
#include "utils.h"


// based on https://iquilezles.org/articles/distfunctions/

struct sdfable
{
  virtual float sdf(const gbl::vec3f& p) const = 0;
};

struct plan : sdfable
{
  gbl::vec3f n;
  float height;

  plan(const gbl::vec3f& normal, float elevation);
  float sdf(const gbl::vec3f& p) const;
};

struct sphere : sdfable
{
  gbl::vec3f c;
  float r;

  sphere(const gbl::vec3f& center, float radius);
  float sdf(const gbl::vec3f& p) const;
};

struct cylinder : sdfable
{
  gbl::vec3f p0, p1;
  float radius;

  cylinder(const gbl::vec3f& a, const gbl::vec3f& b, float r);
  float sdf(const gbl::vec3f& p) const;
};

struct opSub : sdfable
{
  std::shared_ptr<sdfable> h_to_keep, h_to_sub;
  opSub(std::shared_ptr<sdfable> to_keep, std::shared_ptr<sdfable> to_sub);
  float sdf(const gbl::vec3f& p) const;
};

struct opInv : sdfable
{
  std::shared_ptr<sdfable> h;
  opInv(std::shared_ptr<sdfable> to_inv);
  float sdf(const gbl::vec3f& p) const;
};

struct opUnion : sdfable
{
  std::shared_ptr<sdfable> h_1, h_2;
  opUnion(std::shared_ptr<sdfable> h1, std::shared_ptr<sdfable> h2);
  float sdf(const gbl::vec3f& p) const;
};

struct opDisplace : sdfable
{
  std::shared_ptr<sdfable> h;
  std::function<float(const gbl::vec3f&)> f;
  opDisplace(std::shared_ptr<sdfable> to_disp, 
    std::function<float(const gbl::vec3f&)> disp_func);
  float sdf(const gbl::vec3f& p) const;
};
