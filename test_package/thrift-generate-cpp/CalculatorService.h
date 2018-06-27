#include "gen-cpp/Calculator.h"

#include <memory>

class CalculatorService : virtual public CalculatorIf {
 public:
  CalculatorService() {}
  virtual ~CalculatorService() {}
};