#ifndef ENCODER_H
#define ENCODER_H

#include <bitset>
#include <math.h>
#include <algorithm>
#include <numeric>
#include "load.h"


struct Encoded
{
std::vector<int> codewords;
std::vector<std::vector<int>> encodedData;
};

class Encoder
{

public:
    std::string m_fileName;
	int m_sampleNumber;
	std::string m_direction;
	std::vector<int> m_data;
	std::vector<int> m_sampleIndices;

	int m_blockSize;
	std::string m_mode;
	//Encoder();
    Encoder();
    explicit Encoder(int bs, std::string f, int samples, std::string dir, std::string mode);
	void setBlockSize(int bs);
	void printParams();
	void loadData();
	void printData();
	void genSamples(bool random);
	virtual Encoded encode(std::vector<int> &block);
	std::string binaryString(int n);
	virtual int calcBitLength(Encoded encBlock);
	int encodeData();
};

class Delta : public Encoder
{
public:
    using Encoder::Encoder; 
	Encoded encode(std::vector<int> &block);

};

class Golomb : public Encoder
{
    using Encoder::Encoder;
	std::string unary(int n);
	Encoded encode(std::vector<int> &block);
	int calcBitLength(Encoded encBlock);
};

class Simple8b : public Encoder
{
	using Encoder::Encoder;
	Encoded encode(std::vector<int> &block);
	int calcCumBitLength(std::vector<int> deltaVec);
	int calcBitLength(Encoded encBlock);
	int findSelector(int bitLength);
	int bitLengthRound(int bitLength);
};

#endif
