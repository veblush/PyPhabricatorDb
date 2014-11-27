# coding: utf-8
from sqlalchemy import BINARY, Column, Index, Integer, String, VARBINARY
from sqlalchemy import String, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from dbdatetime import dbdatetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Edge(Base):
    __tablename__ = 'edge'
    __table_args__ = (
        Index('src', 'src', 'type', 'dateCreated', 'seq'),
        Index('key_dst', 'dst', 'type', 'src', unique=True)
    )

    src = Column(String, primary_key=True, nullable=False)
    type = Column(Integer, primary_key=True, nullable=False)
    dst = Column(String, primary_key=True, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    seq = Column(Integer, nullable=False)
    dataID = Column(Integer)


class EdgeData(Base):
    __tablename__ = 'edgedata'

    id = Column(Integer, primary_key=True)
    data = Column(Unicode, nullable=False)


class PhortuneAccount(Base):
    __tablename__ = 'phortune_account'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhortuneAccountTransaction(Base):
    __tablename__ = 'phortune_accounttransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhortuneCart(Base):
    __tablename__ = 'phortune_cart'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    accountPHID = Column(String, nullable=False, index=True)
    authorPHID = Column(String, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    status = Column(Unicode(32), nullable=False)
    cartClass = Column(Unicode(128), nullable=False)
    merchantPHID = Column(String, nullable=False, index=True)
    mailKey = Column(BINARY(20), nullable=False)


class PhortuneCartTransaction(Base):
    __tablename__ = 'phortune_carttransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhortuneCharge(Base):
    __tablename__ = 'phortune_charge'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    accountPHID = Column(String, nullable=False, index=True)
    authorPHID = Column(String, nullable=False)
    cartPHID = Column(String, nullable=False, index=True)
    paymentMethodPHID = Column(String)
    amountAsCurrency = Column(Unicode(64), nullable=False)
    status = Column(Unicode(32), nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    merchantPHID = Column(String, nullable=False, index=True)
    providerPHID = Column(String, nullable=False, index=True)
    amountRefundedAsCurrency = Column(Unicode(64), nullable=False)
    refundingPHID = Column(String)
    refundedChargePHID = Column(String)


class PhortuneMerchant(Base):
    __tablename__ = 'phortune_merchant'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    viewPolicy = Column(String, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    description = Column(Unicode, nullable=False)


class PhortuneMerchantTransaction(Base):
    __tablename__ = 'phortune_merchanttransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhortunePaymentMethod(Base):
    __tablename__ = 'phortune_paymentmethod'
    __table_args__ = (
        Index('key_merchant', 'merchantPHID', 'accountPHID'),
        Index('key_account', 'accountPHID', 'status')
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    status = Column(Unicode(64), nullable=False)
    accountPHID = Column(String, nullable=False)
    authorPHID = Column(String, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    brand = Column(Unicode(64), nullable=False)
    expires = Column(Unicode(16), nullable=False)
    lastFourDigits = Column(Unicode(16), nullable=False)
    merchantPHID = Column(String, nullable=False)
    providerPHID = Column(String, nullable=False)


class PhortunePaymentProviderConfig(Base):
    __tablename__ = 'phortune_paymentproviderconfig'
    __table_args__ = (
        Index('key_merchant', 'merchantPHID', 'providerClassKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    merchantPHID = Column(String, nullable=False)
    providerClassKey = Column(BINARY(12), nullable=False)
    providerClass = Column(Unicode(128), nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    isEnabled = Column(Integer, nullable=False)


class PhortunePaymentProviderConfigTransaction(Base):
    __tablename__ = 'phortune_paymentproviderconfigtransaction'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    authorPHID = Column(String, nullable=False)
    objectPHID = Column(String, nullable=False, index=True)
    viewPolicy = Column(String, nullable=False)
    editPolicy = Column(String, nullable=False)
    commentPHID = Column(String)
    commentVersion = Column(Integer, nullable=False)
    transactionType = Column(Unicode(32), nullable=False)
    oldValue = Column(Unicode, nullable=False)
    newValue = Column(Unicode, nullable=False)
    contentSource = Column(Unicode, nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)


class PhortuneProduct(Base):
    __tablename__ = 'phortune_product'
    __table_args__ = (
        Index('key_product', 'productClassKey', 'productRefKey', unique=True),
    )

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)
    productClassKey = Column(BINARY(12), nullable=False)
    productClass = Column(Unicode(128), nullable=False)
    productRefKey = Column(BINARY(12), nullable=False)
    productRef = Column(Unicode(128), nullable=False)


class PhortunePurchase(Base):
    __tablename__ = 'phortune_purchase'

    id = Column(Integer, primary_key=True)
    phid = Column(String, nullable=False, unique=True)
    productPHID = Column(String, nullable=False)
    accountPHID = Column(String, nullable=False)
    authorPHID = Column(String, nullable=False)
    cartPHID = Column(String, index=True)
    basePriceAsCurrency = Column(Unicode(64), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Unicode(32), nullable=False)
    usermetadata = Column('metadata', Unicode, nullable=False)
    dateCreated = Column(dbdatetime, nullable=False)
    dateModified = Column(dbdatetime, nullable=False)