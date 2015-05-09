import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call
import cPickle as pickle

class Slave(Script):

  #Call setup.sh to install the service
  def install(self, env):
  
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    
    #import properties defined in -config.xml file from params class
    import params

    cmd = '/bin/tar' + ' -zxf ' + params.tachyon_package_dir + 'files/' + params.tachyon_archive_file + ' -C  /'
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)
        
    cmd = '/bin/ln' + ' -s ' + params.base_dir + '/tachyon' + ' /usr/hdp/current/'
    Execute('echo "Running ' + cmd + '"')
    # I don't care if the link already exists
    try:
      Execute(cmd)
    except:
      pass

    Directory(params.tachyon_stack_dir,
            recursive=True
    )

    tachyon_config_dir = params.base_dir + 'conf/'
    tachyon_libexec_dir = params.base_dir + 'libexec/'

    File(format("{tachyon_config_dir}/tachyon-env.sh"),
          owner='root',
          group='root',
          content=Template('tachyon-env.sh.j2', conf_dir=tachyon_config_dir)
    )

    File(format("{tachyon_libexec_dir}/tachyon-config.sh"),
          owner='root',
          group='root',
          content=Template('tachyon-config.sh.j2', conf_dir=tachyon_libexec_dir)
    )

  def configure(self, env):
    import params
    env.set_params(params)


  #Call start.sh to start the service
  def start(self, env):

    #import properties defined in -config.xml file from params class
    import params

    #import status properties defined in -config.xml file from status_params class
    #import status_params
    
    #mount ramfs
    cmd = params.base_dir + '/bin/tachyon-start.sh ' + 'worker' + ' Mount'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)

  #Called to stop the service using the pidfile
  def stop(self, env):
  
    #import properties defined in -config.xml file from params class  
    import params

    #import status properties defined in -config.xml file from status_params class  
    #import status_params
    
    #execure the startup script
    cmd = params.base_dir + '/bin/tachyon-stop.sh'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
  
    #call status
    cmd = params.base_dir + '/bin/tachyon ' + 'status ' + 'slave'

    Execute('echo "Running cmd: ' + cmd + '"')
    Execute(cmd)


if __name__ == "__main__":
  Slave().execute()
