#ifndef VEC_H
#define VEC_H

#include <array>
#include <ostream>

namespace gbl
{

  template <unsigned int N, typename T>
    class Vec {
      public:
        Vec() : data{T()} {};
        Vec(const Vec<N, T>& v) = default;
        Vec(Vec<N, T>&& v) = default;

        Vec& operator=(const Vec<N, T>& v) = default;
        Vec& operator=(Vec<N, T>&& v) = default;

        template <typename... Args>
          explicit Vec(Args&&... args) : data{T(args)...}
        {
          static_assert(sizeof...(Args) == N,
              "Invalid number of constructor arguments.");
        }
        template <typename T2>
          explicit Vec(T2 val) {data.fill(val);}
        T& operator[](const unsigned int i) { return data[i]; }
        const T& operator[](const unsigned int i) const { return data[i]; }

        const T& at(const unsigned int i) const { return data.at(i); }

        std::size_t size() const {return N;}

        using value_type = T;

        typename std::array<T, N>::iterator begin() { return data.begin(); }
        typename std::array<T, N>::iterator end() { return data.end(); }
        typename std::array<T, N>::const_iterator begin() const { return data.begin(); }
        typename std::array<T, N>::const_iterator end() const { return data.end(); }
        typename std::array<T, N>::const_iterator cbegin() const { return data.cbegin(); }
        typename std::array<T, N>::const_iterator cend() const { return data.cend(); }

#define SETTER(name, value) template<unsigned int U = N, std::enable_if_t<(U<4 && U>value), bool> = true> T& name() { return data[value]; }
#define GETTER(name, value) template<unsigned int U = N, std::enable_if_t<(U<4 && U>value), bool> = true> T name() const { return data[value]; }

        SETTER(x, 0)  SETTER(y, 1)  SETTER(z, 2)  SETTER(w, 3)
          SETTER(r, 0)  SETTER(g, 1)  SETTER(b, 2)  SETTER(a, 3)
          SETTER(s, 0)  SETTER(t, 1)  SETTER(p, 2)  SETTER(q, 3)

          GETTER(x, 0)  GETTER(y, 1)  GETTER(z, 2)  GETTER(w, 3)
          GETTER(r, 0)  GETTER(g, 1)  GETTER(b, 2)  GETTER(a, 3)
          GETTER(s, 0)  GETTER(t, 1)  GETTER(p, 2)  GETTER(q, 3)

#undef SETTER
#undef GETTER

          template<unsigned int U>
          Vec<U,T> toVecN();

      private:
        std::array<T, N> data;
    };

  using vec2i = Vec<2, int>;
  using vec3u = Vec<3, unsigned int>;
  using vec2f = Vec<2, float>;
  using vec3f = Vec<3, float>;
  using vec4f = Vec<4, float>;
  using vec3 = Vec<3, double>;


  using gbl::Vec;

  template <unsigned int N, typename T>
    Vec<N, T>& operator+=(Vec<N, T>& v1, const Vec<N, T>& v2);
  template <unsigned int N, typename T>
    Vec<N, T>& operator-=(Vec<N, T>& v1, const Vec<N, T>& v2);
  template <unsigned int N, typename T, typename S>
    Vec<N, T>& operator/=(Vec<N, T>& v1, S a);
  template <unsigned int N, typename T, typename S>
    Vec<N, T>& operator*=(Vec<N, T>& v1, S a);

  template <unsigned int N, typename T>
    Vec<N, T> operator+(const Vec<N, T>& v1, const Vec<N, T>& v2);
  template <unsigned int N, typename T>
    Vec<N, T> operator-(const Vec<N, T>& v1, const Vec<N, T>& v2);
  template <unsigned int N, typename T, typename S>
    Vec<N, T> operator/(const Vec<N, T>& v1, S a);
  template <unsigned int N, typename T, typename S>
    Vec<N, T> operator*(const Vec<N, T>& v5, S a);
  template <unsigned int N, typename T, typename S>
    Vec<N, T> operator*(S a, const Vec<N, T>& v1);

  template <unsigned int N, typename T>
    Vec<N, T> operator*(const Vec<N, T>& v1, const Vec<N, T>& v2);

  template <unsigned int N, typename T>
    Vec<N, T> min(const Vec<N, T>& v1, const Vec<N, T>& v2);
  template <unsigned int N, typename T>
    Vec<N, T> max(const Vec<N, T>& v1, const Vec<N, T>& v2);

  template <unsigned int N, typename T>
    T dot(const Vec<N, T>& vec, const Vec<N, T>& vec2);
  template <unsigned int N, typename T>
    T norm2(const Vec<N, T>& vec);
  template <unsigned int N, typename T>
    T norm(const Vec<N, T>& vec);
  template <unsigned int N, typename T>
    Vec<N, T> normalize(const Vec<N, T>& vec);

  template <unsigned int N, typename T>
    std::string to_string(const Vec<N, T>& v);

  template <unsigned int N, typename T>
    Vec<N, T> floor(const Vec<N, T>& v);

  template <unsigned int N, typename T>
    Vec<N, T> fract(const Vec<N, T>& v);
}

template <unsigned int N, typename T>
std::ostream& operator<<(std::ostream& os, const gbl::Vec<N, T>& v);

#include "vec.ipp"

extern template class gbl::Vec<2, int>;
extern template class gbl::Vec<3, unsigned int>;
extern template class gbl::Vec<2, float>;
extern template class gbl::Vec<3, float>;
extern template class gbl::Vec<4, float>;
extern template class gbl::Vec<3, double>;

#endif
