#include <cmath>
#include <istream>

  template <unsigned int N, typename T>
gbl::Vec<N, T>& gbl::operator+=(gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  for (auto i = 0u; i < N; ++i) {
    v1[i] += v2[i];
  }
  return v1;
}
  template <unsigned int N, typename T>
gbl::Vec<N, T>& gbl::operator-=(gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  for (auto i = 0u; i < N; ++i) {
    v1[i] -= v2[i];
  }
  return v1;
}
  template <unsigned int N, typename T, typename S>
gbl::Vec<N, T>& gbl::operator/=(gbl::Vec<N, T>& v1, S a)
{
  for (auto i = 0u; i < N; ++i) {
    v1[i] /= a;
  }
  return v1;
}
  template <unsigned int N, typename T, typename S>
gbl::Vec<N, T>& gbl::operator*=(gbl::Vec<N, T>& v1, S a)
{
  for (auto i = 0u; i < N; ++i) {
    v1[i] *= a;
  }
  return v1;
}
  template <unsigned int N, typename T>
gbl::Vec<N, T> gbl::operator+(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  auto tmp = v1;
  tmp += v2;
  return tmp;
}
  template <unsigned int N, typename T>
gbl::Vec<N, T> gbl::operator-(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  auto tmp = v1;
  tmp -= v2;
  return tmp;
}
  template <unsigned int N, typename T, typename S>
gbl::Vec<N, T> gbl::operator/(const gbl::Vec<N, T>& v1, S a)
{
  auto tmp = v1;
  tmp /= a;
  return tmp;
}
  template <unsigned int N, typename T, typename S>
gbl::Vec<N, T> gbl::operator*(const gbl::Vec<N, T>& v1, S a)
{
  auto tmp = v1;
  tmp *= a;
  return tmp;
}
  template <unsigned int N, typename T, typename S>
gbl::Vec<N, T> gbl::operator*(S a, const gbl::Vec<N, T>& v1)
{
  return v1 * a;
}

  template <unsigned int N, typename T>
gbl::Vec<N, T> gbl::operator*(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  auto ans = v1;
  for (auto i = 0u; i < N; ++i) {
    ans[i] *= v2[i];
  }
  return v1;
}
  template <unsigned int N, typename T>
gbl::Vec<N, T> gbl::min(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  gbl::Vec<N, T> v;
  for (auto i = 0u; i < N; ++i)
    v[i] = std::min(v1[i], v2[i]);
  return v;
}
  template <unsigned int N, typename T>
gbl::Vec<N, T> gbl::max(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  gbl::Vec<N, T> v;
  for (auto i = 0u; i < N; ++i)
    v[i] = std::max(v1[i], v2[i]);
  return v;
}
  template <unsigned int N, typename T>
T gbl::dot(const gbl::Vec<N, T>& v1, const gbl::Vec<N, T>& v2)
{
  T sum = T();

  for (auto i = 0u; i < N; ++i) {
    sum += v1[i] * v2[i];
  }
  return sum;
}
  template <unsigned int N>
float gbl::norm2(const gbl::Vec<N, float>& v)
{
  return dot(v,v);
}
  template <unsigned int N>
float gbl::norm(const gbl::Vec<N, float>& v)
{
  return std::sqrt(norm2(v));
}
  template <unsigned int N>
gbl::Vec<N, float> gbl::normalize(const gbl::Vec<N, float>& v)
{
  const float n = norm(v);
  return v/n;
}
  template <unsigned int N>
gbl::Vec<N, float> gbl::floor(const Vec<N, float>& v)
{
  auto ans = v;
  for(auto& x:ans)
    x = std::floor(x);
  return ans;
}
  template <unsigned int N>
gbl::Vec<N, float> gbl::fract(const Vec<N, float>& v)
{
  return v-gbl::floor(v);
}
  template <unsigned int N, typename T>
std::ostream& operator<<(std::ostream& os, const gbl::Vec<N, T>& v)
{
  for (auto i = 0u; i < N; ++i) {
    os << v[i] << (i == N-1 ? "" : " ");
  }
  return os;
}
  template <unsigned int N, typename T>
std::string to_string(const gbl::Vec<N, T>& v)
{
  std::string str;
  for (auto i = 0u; i < N; ++i) {
    str += std::to_string(v[i]) + (i == N-1 ? "" : " ");
  }
  return str;
}
template<unsigned int N, typename T>
  template< unsigned int U>
gbl::Vec<U,T> gbl::Vec<N,T>::toVecN()
{
  gbl::Vec<U,T> v{T()};
  if constexpr(U > N)
    std::copy(data.begin(), data.end(), v.begin());
  else
    std::copy(data.begin(), data.begin()+U, v.begin());
  return v;
}
