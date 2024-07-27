#include "BinPtracFixture.hpp"

TEST_F(BinPtracFixture, BinPtracEventTime) {
  std::vector<mcnptools::PtracHistory> hists = ptrac.ReadHistories(1);

  mcnptools::PtracEvent e = hists.at(0).GetEvent(0);

  EXPECT_EQ(e.Get(mcnptools::Ptrac::TIME), 0.0);
}
