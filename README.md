<h3 align="center">AWS EBS Volume Cost Calculation</h3>

---

<p align="center"> This is a Python script to calculate the costs associated with Amazon Elastic Block Store (EBS) volumes in the Amazon Web Services (AWS) cloud.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Library Installation](#library-installation)
- [Execution](#execution)
- [Result](#result)
- [Author](#author)

## 🧐 About <a name="about"></a>

This Python script enables you to calculate the costs associated with AWS EBS volumes. It identifies attached EBS volumes using the 'gp2' volume type and calculates the cost difference when migrating these volumes to the 'gp3' type. Additionally, it also calculates the total cost of available EBS volumes.

## 🚀 How It Works <a name="how-it-works"></a>

1. Make sure you have your AWS profile configured on your machine.
2. Download the `cost_ebs.py` script.
3. Run the script by passing the AWS region as a command-line argument: `python3 cost_ebs.py REGION_CODE`, where REGION_CODE is the desired AWS region.

## Prerequisites <a name="prerequisites"></a>

Make sure you have the following installed on your machine:
- [Python](https://www.python.org/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Pandas](https://pandas.pydata.org/)

## Library Installation <a name="library-installation"></a>

To install the necessary libraries, you can execute the following command:

```shell
pip install boto3 pandas
```

## 🚀 Execution <a name="execution"></a>

After having the libraries installed and your AWS profile configured, you can execute the cost_ebs.py script. Use the following command in the terminal:

```shell
python3 cost_ebs.py REGION_CODE
```

## 📊 Result <a name="result"></a>

After running the script, it will calculate and display the total cost of available EBS volumes and the potential savings when migrating 'gp2' volumes to 'gp3'. Additionally, the script will generate an Excel file named ebs_volumes.xlsx, containing detailed information about the costs of the volumes.

The results provided by the script are a valuable tool for understanding the costs associated with EBS volumes in the specified region. You can use these results to optimize your storage resources in AWS and make informed decisions about volume type migration.

## ✍️ Author <a name="author"></a>

- Matheus Basilio Cintra - [@MatheusBasilio](https://github.com/MatheusBasilio)




