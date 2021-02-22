'''
	From https://github.com/dathlin/HslCommunicationPython
	(pip install HslCommunication==1.0.4)
'''
from ._hsl import HslProtocol, HslSecurity, OperateResult, StringResources
from .BasicFramework import SoftBasic

from . import (
	BasicFramework,
	Language,
	Core,
	Modbus,
	Enthernet,
	Profinet,
	client,
)

'''
             ///\      ///\             /////////\              ///\
            //\\/      //\/           //\\\\\\\\//\            //\\/
           //\/       //\/          //\\/       \\/           //\/
          //\/       //\/           \//\                     //\/
         /////////////\/             \//////\               //\/
        //\\\\\\\\\//\/               \\\\\//\             //\/
       //\/       //\/                     \//\           //\/
      //\/       //\/           ///\      //\\/          //\/       //\
     ///\      ///\/            \/////////\\/           /////////////\/
     \\\/      \\\/              \\\\\\\\\/             \\\\\\\\\\\\\/             Present by Richard.Hu

	CopyRight by Richard.Hu 2017-2020
	 本程序的版权归胡少林所有，源代码仅限于学术研究使用，商用需要授权，在没有获得商用版权的情况下，应用于商用项目，将依法追究法律责任，感谢支持，详细说明请参照：

	 企业商用说明：仅限于公司开发的软件，该软件的署名必须为授权公司，不得改成他人或是公司（除非他人或公司已经取得商用授权），该软件不能被转卖。授权不限制项目，一次授权，终生使用。

	 关于授权的步骤：
	     1. 签合同，双方在合同上签字
		 2. 付款，支持支付宝，微信，银行卡
		 3. 开发票，增值税普票（个人找税务局代开的）
		 4. 加入 Hsl超级VIP群 即获得源代码和超级激活码，永久支持更新。
		 5. 注册官网的git账户
		 6. 专业培训额外付费，1000元人民币1小时，培训控件使用，控件开发。
		 7. 联系方式：Email:hsl200909@163.com   QQ:200962190   Weichat:13516702732

	官网：http://www.hslcommunication.cn  如果不能访问，请访问：http://118.24.36.220


	The copyright of this program belongs to Hu Shaolin. The source code is limited to academic research. Commercial licenses are required. 
	If commercial copyrights are not obtained and applied to commercial projects, legal liability will be investigated. Thank you for your support. For details, please refer to:


	Personal commercial description: It is limited to software developed by individuals. The software must be signed by an authorized person. 
	It must not be changed to another person or company (unless another person or company has obtained a commercial license). 
	The software cannot be resold. Authorization does not limit the project, once authorized, lifetime use.

	Enterprise commercial description: It is limited to the software developed by the company. The signature of the software must be an authorized company. 
	It must not be changed to another person or company (unless someone else or the company has obtained a commercial license). The software cannot be resold. 
	Authorization does not limit the project, once authorized, lifetime use.

	Steps on authorization:
	1. Sign the contract, both parties sign the contract
	2. Payment, support Alipay, WeChat, bank card
	3. Invoice, general VAT ticket (issued on behalf of the individual, registered companies will be different later)
	4. Join the Hsl Super VIP Group to get the source code and super activation code, and always support updates.
	5. Register git account on official website
	6. Professional training costs an additional fee of 1,000 yuan per hour, training controls use, control development.
	7. Contact: Email: hsl200909@163.com QQ: 200962190 Weichat: 13516702732
	
	Website：http://www.hslcommunication.cn  If you cannot access, please visit: http://118.24.36.220

'''