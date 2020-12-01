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
	std::vector<std::vector<int>> m_allData;
	std::vector<int> m_sampleIndices;
	int m_blockSize;
	std::string m_mode;
	float m_compressionRatio;
	int m_bits;
	int m_iterations;
    Encoder();
   
    explicit Encoder(int bs, std::string f, int samples, std::string dir, std::string mode, int bits, int iterations);
	Encoder *makeEncoder(std::string choice);
	void setBlockSize(int bs);
	void printParams();
	void setDirection(std::string dir);
	void loadData();
	void printData();
	float getCompressionRatio();
	int getDataLength();
	void genSamples(bool random);
	virtual Encoded encode(std::vector<int> &block);
	std::string binaryString(int n);
	virtual int calcBitLength(Encoded encBlock);
	int encodeData(bool decodeFlag);
	virtual std::vector<int> decode(Encoded encodedBlock);
};

class Delta : public Encoder
{
public:
    using Encoder::Encoder; 
	Encoded encode(std::vector<int> &block);
	std::vector<int> decode(Encoded encodedBlock);
};

class Golomb : public Encoder
{
    using Encoder::Encoder;
	std::string unary(int n);
	Encoded encode(std::vector<int> &block);
	std::vector<int> decode(Encoded encodedBlock);
	int calcBitLength(Encoded encBlock);
};

class StepDelta : public Encoder
{
    using Encoder::Encoder;
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

class DeltaDelta : public Encoder
{
public:
    using Encoder::Encoder; 
	Encoded encode(std::vector<int> &block);
	std::vector<int> decode(Encoded encodedBlock);
};

class DeltaGolomb : public Golomb
{
public:
	using Golomb::Golomb;
	Encoded encode(std::vector<int> &block);
};

class DeltaIter : public Encoder
{
public:
	using Encoder::Encoder;
	Encoded encode(std::vector<int> &block);
	void difference(std::vector<int> &codeVec, std::vector<int> &deltaVec);
};
#endif

