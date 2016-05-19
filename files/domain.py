ORACLE_HOME = '/opt/oraclefmw/product/oracle_home'
WLHOME      = ORACLE_HOME+'/wlserver'
DOMAIN      = 'domain1'
DOMAIN_PATH = '/opt/oraclefmw/config/domains/' + DOMAIN
APP_PATH    = '/opt/oraclefmw/config/applications/' + DOMAIN

ADMIN_SERVER_ADDRESS = 'admin-server-host'
LOG_FOLDER     = '/opt/oraclefmw/weblogic/'

# Expanded or Compact
DOMAIN_MODE = 'Expanded'
JSSE_ENABLED     = true
DEVELOPMENT_MODE = true
WEBTIER_ENABLED  = false

ADMIN_SERVER   = 'AdminServer'
ADMIN_USER     = 'weblogic'
ADMIN_PASSWORD = 'welcome1'

JAVA_HOME      = '/usr/java/latest'

ADM_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+LOG_FOLDER+'AdminServer_err.out'

def createBootPropertiesFile(directoryPath,fileName, username, password):
    serverDir = File(directoryPath)
    bool = serverDir.mkdirs()
    fileNew=open(directoryPath + '/'+fileName, 'w')
    fileNew.write('username=%s\n' % username)
    fileNew.write('password=%s\n' % password)
    fileNew.flush()
    fileNew.close()

def createAdminStartupPropertiesFile(directoryPath, args):
    adminserverDir = File(directoryPath)
    bool = adminserverDir.mkdirs()
    fileNew=open(directoryPath + '/startup.properties', 'w')
    args=args.replace(':','\\:')
    args=args.replace('=','\\=')
    fileNew.write('Arguments=%s\n' % args)
    fileNew.flush()
    fileNew.close()

print('Start...wls domain with template ORACLE_HOME/wlserver/common/templates/wls/wls.jar')
readTemplate(ORACLE_HOME+'/wlserver/common/templates/wls/wls.jar', DOMAIN_MODE)


cd('/')

print('Set domain log')
create('base_domain','Log')

cd('/Log/base_domain')
set('FileName'    ,LOG_FOLDER+DOMAIN+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

cd('/Servers/AdminServer')
# name of adminserver
set('Name',ADMIN_SERVER )

cd('/Servers/'+ADMIN_SERVER)

# address and port
set('ListenAddress',ADMIN_SERVER_ADDRESS)
set('ListenPort'   ,7001)

setOption( "AppDir", APP_PATH )

create(ADMIN_SERVER,'ServerStart')
cd('ServerStart/'+ADMIN_SERVER)
set('Arguments' , ADM_JAVA_ARGUMENTS)
set('JavaVendor','Sun')
set('JavaHome'  , JAVA_HOME)

cd('/Server/'+ADMIN_SERVER)
create(ADMIN_SERVER,'SSL')
cd('SSL/'+ADMIN_SERVER)
set('Enabled'                    , 'False')
set('HostNameVerificationIgnored', 'True')

if JSSE_ENABLED == true:
    set('JSSEEnabled','True')
else:
    set('JSSEEnabled','False')


cd('/Server/'+ADMIN_SERVER)

create(ADMIN_SERVER,'Log')
cd('/Server/'+ADMIN_SERVER+'/Log/'+ADMIN_SERVER)
set('FileName'    ,LOG_FOLDER+ADMIN_SERVER+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

print('Set password...')
cd('/')
cd('Security/base_domain/User/weblogic')

# weblogic user name + password
set('Name',ADMIN_USER)
cmo.setPassword(ADMIN_PASSWORD)

if DEVELOPMENT_MODE == true:
    setOption('ServerStartMode', 'dev')
else:
    setOption('ServerStartMode', 'prod')

setOption('JavaHome', JAVA_HOME)

print('write domain...')
# write path + domain name
writeDomain(DOMAIN_PATH)
closeTemplate()

createAdminStartupPropertiesFile(DOMAIN_PATH+'/servers/'+ADMIN_SERVER+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DOMAIN_PATH+'/servers/'+ADMIN_SERVER+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DOMAIN_PATH+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

print('Exiting WebLogic Domain creation completed ...')
exit()
