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
    Encoder();
    explicit Encoder(int bs, std::string f, int samples, std::string dir, std::string mode);
	void setBlockSize(int bs);
	void printParams();
	void setDirection(std::string dir);
	void loadData();
	void printData();
	float getCompressionRatio();
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

#endif
