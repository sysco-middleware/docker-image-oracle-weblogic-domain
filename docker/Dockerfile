FROM tmp-oracle-wls-domain

MAINTAINER Jorge Quilcate <jorge.quilcate@sysco.no>

USER oraclefmw

ENV DOMAIN_HOME=/opt/oraclefmw/config/domains/domain1 \
    ORACLE_HOME=/opt/oraclefmw/product/oracle_home \
    DOMAIN_NAME=domain1


WORKDIR $DOMAIN_HOME

CMD sed -i "s/admin-server-host/$HOSTNAME/g" config/config.xml && \
    sh startWebLogic.sh
