/*
 * Author: Jensen Holm
 * Date: March 2024
*/

#include "./DataFrame/DataFrame.hpp"
#include <iostream>

int main(int argc, char* argv[]) {
  // first command line argument should be a csv file path
  std::string fp = std::string(argv[1]);
  DataFrame df(fp);
  return 0;
}

