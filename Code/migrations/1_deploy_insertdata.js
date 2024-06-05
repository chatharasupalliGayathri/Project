const insertdata=artifacts.require('insertdata')
module.exports=function(deployer)
{
    deployer.deploy(insertdata);
}