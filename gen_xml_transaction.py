from datetime import datetime
import xml.dom.minidom
import logging

class xml_gen():
    def __init__(self):
        self.log = logging.getLogger("xml_gen")

    def add_element(self, doc, namenode1, namespace, namenode2, text):
            namenode = doc.createElement(namespace + ":" + namenode2)
            if text != None:
                namenodeTextNode = doc.createTextNode(text)
                namenode.appendChild(namenodeTextNode)
            namenode1.appendChild(namenode)

    def create_element(self, doc, nameNode1, namespace, text):
            namenode = doc.createElement(namespace)
            if text != None:
                namenodeTextNode = doc.createTextNode(text)
                namenode.appendChild(namenodeTextNode)
            nameNode1.appendChild(namenode)


    def get_text_node(self, xml_str, namespace, name):
        xml_obj = xml.dom.minidom.parseString(xml_str)
        try:
            value = xml_obj.getElementsByTagNameNS(namespace, name)[0].firstChild.nodeValue
        except:
            value = None
        return value


    def AcceptorAuthorisationRequest(self, datetime, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxDtls):
        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorAuthorisationRequest = doc.createElement('ns17:AcceptorAuthorisationRequest')
        AcceptorAuthorisationRequest.setAttribute("xmlns", "http://schemas.bssys.com/iso20022/service/common/v1")
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns17','http://schemas.bssys.com/iso20022/service/messages/v1')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns10' , 'urn:iso:std:iso:20022:tech:xsd:caaa.007.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns11' , 'urn:iso:std:iso:20022:tech:xsd:caaa.008.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns12' , 'urn:iso:std:iso:20022:tech:xsd:caaa.009.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns13' , 'urn:iso:std:iso:20022:tech:xsd:caaa.010.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns14' , 'urn:iso:std:iso:20022:tech:xsd:caaa.013.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns15' , 'urn:iso:std:iso:20022:tech:xsd:caaa.014.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns16' , 'urn:iso:std:iso:20022:tech:xsd:caaa.015.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns2' , 'urn:iso:std:iso:20022:tech:xsd:caaa.001.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns3' , 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns4' , 'urn:iso:std:iso:20022:tech:xsd:caaa.005.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns5' , 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns6' , 'urn:iso:std:iso:20022:tech:xsd:caaa.011.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns7' , 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns8' , 'urn:iso:std:iso:20022:tech:xsd:caaa.003.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns9' , 'urn:iso:std:iso:20022:tech:xsd:caaa.004.001.01')
    
        AccptrAuthstnReq = doc.createElement('ns2:AccptrAuthstnReq')
        AcceptorAuthorisationRequest.appendChild(AccptrAuthstnReq)

        Hdr = doc.createElement('ns2:Hdr')
        AccptrAuthstnReq.appendChild(Hdr)
        self.add_element(doc, Hdr, 'ns2', 'MsgFctn', 'AUTQ')
        self.add_element(doc, Hdr, 'ns2', 'PrtcolVrsn', '01.00')
        self.add_element(doc, Hdr, 'ns2', 'XchgId', '0')
        self.add_element(doc, Hdr, 'ns2', 'CreDtTm', str(datetime))

        InitgPtyNode = doc.createElement('ns2:InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.add_element(doc, InitgPtyNode, 'ns2', 'Id', InitgPty)

        AuthstnReq = doc.createElement('ns2:AuthstnReq')
        AccptrAuthstnReq.appendChild(AuthstnReq)

        Envt = doc.createElement('ns2:Envt')
        AuthstnReq.appendChild(Envt)

        MrchntNode = doc.createElement('ns2:Mrchnt')
        Envt.appendChild(MrchntNode) 
        MrchntIdNode = doc.createElement('ns2:Id')
        MrchntNode.appendChild(MrchntIdNode)
        self.add_element(doc, MrchntIdNode, 'ns2', 'Id', Mrchnt)

        POI = doc.createElement('ns2:POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('ns2:Id')
        POI.appendChild(POIIdNode)
        self.add_element(doc, POIIdNode, 'ns2', 'Id', POI_id)

        Card = doc.createElement('ns2:Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('ns2:PlainCardData')
        Card.appendChild(PlainCardData)
        self.add_element(doc, PlainCardData, 'ns2', 'PAN', PAN)
        self.add_element(doc, PlainCardData, 'ns2', 'XpryDt', XpryDt)
        self.add_element(doc, Card, 'ns2', 'CardPdctPrfl', '0060')
        self.add_element(doc, Card, 'ns2', 'AddtlCardData', AddtlCardData)

        Cntxt = doc.createElement('ns2:Cntxt')
        AuthstnReq.appendChild(Cntxt)
        PmtCntxt = doc.createElement('ns2:PmtCntxt')
        Cntxt.appendChild(PmtCntxt)
        self.add_element(doc, PmtCntxt, 'ns2', 'CardDataNtryMd', 'BRCD')
        SaleCntxt = doc.createElement('ns2:SaleCntxt')
        Cntxt.appendChild(SaleCntxt)

        Tx = doc.createElement('ns2:Tx')
        AuthstnReq.appendChild(Tx)
        self.add_element(doc, Tx, 'ns2', 'TxCaptr', 'true')
        self.add_element(doc, Tx, 'ns2', 'TxTp', 'CRDP')
        self.add_element(doc, Tx, 'ns2', 'SvcAttr', 'IRES')
        self.add_element(doc, Tx, 'ns2', 'MrchntCtgyCdTp', '5411')

        TxId = doc.createElement('ns2:TxId')
        Tx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns2', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns2', 'TxRef', TxRef)

        TxDtlsNode = doc.createElement('ns2:TxDtls')
        Tx.appendChild(TxDtlsNode)
        Ccy = TxDtls['Ccy']
        TtlAmt = TxDtls['TtlAmt']
        self.add_element(doc, TxDtlsNode, 'ns2', 'Ccy', str(Ccy))
        self.add_element(doc, TxDtlsNode, 'ns2', 'TtlAmt', str(TtlAmt))
        for TxDlsEl in TxDtls['Pdct']:
            Pdct = doc.createElement('ns2:Pdct')
            TxDtlsNode.appendChild(Pdct)
            self.add_element(doc, Pdct, 'ns2', 'PdctCd', str(TxDlsEl['PdctCd']))
            self.add_element(doc, Pdct, 'ns2', 'UnitOfMeasr', str(TxDlsEl['UnitOfMeasr']))
            self.add_element(doc, Pdct, 'ns2', 'PdctQty', str(TxDlsEl['PdctQty']))
            self.add_element(doc, Pdct, 'ns2', 'UnitPric', str(TxDlsEl['UnitPric']))
            self.add_element(doc, Pdct, 'ns2', 'PdctAmt', str(TxDlsEl['PdctAmt']))

        SctyTrlr = doc.createElement('ns2:SctyTrlr')
        AccptrAuthstnReq.appendChild(SctyTrlr)
        self.add_element(doc, SctyTrlr, 'ns2', 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorAuthorisationRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))


    def AcceptorBatchTransferRequest(self, datetime, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxDtls, Nm, code):

        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorBatchTransferRequest = doc.createElement('ns17:AcceptorBatchTransferRequest')
        AcceptorBatchTransferRequest.setAttribute("xmlns", "http://schemas.bssys.com/iso20022/service/common/v1")
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns17','http://schemas.bssys.com/iso20022/service/messages/v1')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns10' , 'urn:iso:std:iso:20022:tech:xsd:caaa.007.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns11' , 'urn:iso:std:iso:20022:tech:xsd:caaa.008.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns12' , 'urn:iso:std:iso:20022:tech:xsd:caaa.009.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns13' , 'urn:iso:std:iso:20022:tech:xsd:caaa.010.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns14' , 'urn:iso:std:iso:20022:tech:xsd:caaa.013.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns15' , 'urn:iso:std:iso:20022:tech:xsd:caaa.014.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns16' , 'urn:iso:std:iso:20022:tech:xsd:caaa.015.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns2' , 'urn:iso:std:iso:20022:tech:xsd:caaa.001.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns3' , 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns4' , 'urn:iso:std:iso:20022:tech:xsd:caaa.005.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns5' , 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns6' , 'urn:iso:std:iso:20022:tech:xsd:caaa.011.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns7' , 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns8' , 'urn:iso:std:iso:20022:tech:xsd:caaa.003.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns9' , 'urn:iso:std:iso:20022:tech:xsd:caaa.004.001.01')
    
        AccptrBtchTrf = doc.createElement('ns6:AccptrBtchTrf')
        AcceptorBatchTransferRequest.appendChild(AccptrBtchTrf)

        Hdr = doc.createElement('ns6:Hdr')
        AccptrBtchTrf.appendChild(Hdr)
        self.add_element(doc, Hdr, 'ns6', 'DwnldTrf', 'false')
        self.add_element(doc, Hdr, 'ns6', 'FrmtVrsn', '01.00')
        self.add_element(doc, Hdr, 'ns6', 'XchgId', '45')
        self.add_element(doc, Hdr, 'ns6', 'CreDtTm', str(datetime))

        InitgPtyNode = doc.createElement('ns6:InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.add_element(doc, InitgPtyNode, 'ns6', 'Id', InitgPty)

        DataSet = doc.createElement('ns6:DataSet')
        AccptrBtchTrf.appendChild(DataSet)

        DataSetId = doc.createElement('ns6:DataSetId')
        DataSet.appendChild(DataSetId)
        self.add_element(doc, DataSetId, 'ns6', 'Nm', Nm)
        self.add_element(doc, DataSetId, 'ns6', 'Tp', 'TXCP')
        self.add_element(doc, DataSetId, 'ns6', 'CreDtTm', str(datetime))

        TxTtls = doc.createElement('ns6:TxTtls')
        DataSet.appendChild(TxTtls)
        Ccy = TxDtls['Ccy']
        summary = TxDtls['TtlAmt']
        self.add_element(doc, TxTtls, 'ns6', 'Ccy', str(Ccy))
        self.add_element(doc, TxTtls, 'ns6', 'Tp', 'DEBT')
        self.add_element(doc, TxTtls, 'ns6', 'TtlNb', '1')
        self.add_element(doc, TxTtls, 'ns6', 'CmltvAmt', str(summary))

        TxToCaptr = doc.createElement('ns6:TxToCaptr')
        DataSet.appendChild(TxToCaptr)
        self.add_element(doc, TxToCaptr, 'ns6', 'TxSeqCntr', '1')
        Envt = doc.createElement('ns6:Envt')
        TxToCaptr.appendChild(Envt)

        shop = doc.createElement('ns6:Mrchnt')
        Envt.appendChild(shop)
        merch_Id = doc.createElement('ns6:Id')
        shop.appendChild(merch_Id)
        self.add_element(doc, merch_Id, 'ns6', 'Id', Mrchnt)

        POI = doc.createElement('ns6:POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('ns6:Id')
        POI.appendChild(POIIdNode)
        self.add_element(doc, POIIdNode, 'ns6', 'Id', POI_id)

        Card = doc.createElement('ns6:Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('ns6:PlainCardData')
        Card.appendChild(PlainCardData)
        self.add_element(doc, PlainCardData, 'ns6', 'PAN', PAN)
        self.add_element(doc, PlainCardData, 'ns6', 'XpryDt', XpryDt)
        self.add_element(doc, Card, 'ns2', 'CardPdctPrfl', '0060')
        self.add_element(doc, Card, 'ns2', 'AddtlCardData', AddtlCardData)

        Tx = doc.createElement('ns6:Tx')
        TxToCaptr.appendChild(Tx)
        self.add_element(doc, Tx, 'ns6', 'TxTp', 'CRDP')
        self.add_element(doc, Tx, 'ns6', 'SvcAttr', 'IRES')
        self.add_element(doc, Tx, 'ns6', 'MrchntCtgyCdTp', '5411')

        TxId = doc.createElement('ns6:TxId')
        Tx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns6', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns6', 'TxRef', TxRef)

        OrgnlTx = doc.createElement('ns6:OrgnlTx')
        Tx.appendChild(OrgnlTx)
        TxId = doc.createElement('ns6:TxId')
        OrgnlTx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns6', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns6', 'TxRef', TxRef)

        POIId = doc.createElement('ns6:POIId')
        OrgnlTx.appendChild(POIId)
        self.add_element(doc, POIId, 'ns6', 'Id', POI_id)
        self.add_element(doc, OrgnlTx, 'ns6', 'TxTp', 'CRDP')

        TxRslt = doc.createElement('ns6:TxRslt')
        OrgnlTx.appendChild(TxRslt)
        RspnToAuthstn = doc.createElement('ns6:RspnToAuthstn')
        TxRslt.appendChild(RspnToAuthstn)
        self.add_element(doc, RspnToAuthstn, 'ns6', 'Rspn', 'APPR')
        self.add_element(doc, TxRslt, 'ns6', 'AuthstnCd', code)
        self.add_element(doc, Tx, 'ns6', 'TxSucss', 'true')

        TxDtls = doc.createElement('ns6:TxDtls')
        Tx.appendChild(TxDtls)
        self.add_element(doc, TxDtls, 'ns6', 'Ccy', str(Ccy)) # Код соц программы
        self.add_element(doc,TxDtls, 'ns6', 'TtlAmt', str(summary)) # Общая сумма транзакции


        SctyTrlr = doc.createElement('ns6:SctyTrlr')
        AccptrBtchTrf.appendChild(SctyTrlr)
        self.add_element(doc, SctyTrlr, 'ns2', 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorBatchTransferRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))
    
    def AcceptorCancellationRequest(self, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxRefNode, TxDtTmNode, AuthstnCd, Ccy, TtlAmt):
        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorCancellationRequest = doc.createElement('ns17:AcceptorCancellationRequest')
        AcceptorCancellationRequest.setAttribute("xmlns","http://schemas.bssys.com/iso20022/service/common/v1")
        AcceptorCancellationRequest.setAttribute('xmlns:ns17','http://schemas.bssys.com/iso20022/service/messages/v1')
        AcceptorCancellationRequest.setAttribute('xmlns:ns10' , 'urn:iso:std:iso:20022:tech:xsd:caaa.007.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns11' , 'urn:iso:std:iso:20022:tech:xsd:caaa.008.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns12' , 'urn:iso:std:iso:20022:tech:xsd:caaa.009.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns13' , 'urn:iso:std:iso:20022:tech:xsd:caaa.010.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns14' , 'urn:iso:std:iso:20022:tech:xsd:caaa.013.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns15' , 'urn:iso:std:iso:20022:tech:xsd:caaa.014.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns16' , 'urn:iso:std:iso:20022:tech:xsd:caaa.015.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns2' , 'urn:iso:std:iso:20022:tech:xsd:caaa.001.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns3' , 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns4' , 'urn:iso:std:iso:20022:tech:xsd:caaa.005.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns5' , 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns6' , 'urn:iso:std:iso:20022:tech:xsd:caaa.011.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns7' , 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns8' , 'urn:iso:std:iso:20022:tech:xsd:caaa.003.001.01')
        AcceptorCancellationRequest.setAttribute('xmlns:ns9' , 'urn:iso:std:iso:20022:tech:xsd:caaa.004.001.01')

        AccptrCxlReq = doc.createElement('ns4:AccptrCxlReq')
        AcceptorCancellationRequest.appendChild(AccptrCxlReq)

        Hdr = doc.createElement('ns4:Hdr')
        AccptrCxlReq.appendChild(Hdr)
        self.add_element(doc, Hdr, 'ns4', 'MsgFctn', 'CCAQ')
        self.add_element(doc, Hdr, 'ns4', 'PrtcolVrsn', '1.00')
        self.add_element(doc, Hdr, 'ns4', 'XchgId', '1')
        self.add_element(doc, Hdr, 'ns4', 'CreDtTm', datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00')

        InitgPtyNode = doc.createElement('ns4:InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.add_element(doc, InitgPtyNode, 'ns4', 'Id', InitgPty)

        CxlReq = doc.createElement('ns4:CxlReq')
        AccptrCxlReq.appendChild(CxlReq)

        Envt = doc.createElement('ns4:Envt')
        CxlReq.appendChild(Envt)

        MrchntNode = doc.createElement('ns4:Mrchnt')
        Envt.appendChild(MrchntNode)
        MrchntIdNode = doc.createElement('ns4:Id')
        MrchntNode.appendChild(MrchntIdNode)
        self.add_element(doc, MrchntIdNode, 'ns4', 'Id', Mrchnt)

        POI = doc.createElement('ns4:POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('ns4:Id')
        POI.appendChild(POIIdNode)
        self.add_element(doc, POIIdNode, 'ns4', 'Id', POI_id)

        Card = doc.createElement('ns4:Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('ns4:PlainCardData')
        Card.appendChild(PlainCardData)
        self.add_element(doc, PlainCardData, 'ns4', 'PAN', PAN)
        self.add_element(doc, PlainCardData, 'ns4', 'XpryDt', XpryDt)
        self.add_element(doc, Card, 'ns4', 'CardPdctPrfl', '0060')
        self.add_element(doc, Card, 'ns4', 'AddtlCardData', AddtlCardData)

        Cntxt = doc.createElement('ns4:Cntxt')
        CxlReq.appendChild(Cntxt)
        PmtCntxt = doc.createElement('ns4:PmtCntxt')
        Cntxt.appendChild(PmtCntxt)
        self.add_element(doc, PmtCntxt, 'ns4', 'CardDataNtryMd', 'BRCD')
        SaleCntxt = doc.createElement('ns4:SaleCntxt')
        Cntxt.appendChild(SaleCntxt)

        Tx = doc.createElement('ns4:Tx')
        CxlReq.appendChild(Tx)
        self.add_element(doc, Tx, 'ns4', 'TxCaptr', 'true')
        self.add_element(doc, Tx, 'ns4', 'MrchntCtgyCd', '5411')

        TxId = doc.createElement('ns4:TxId')
        Tx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns4', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns4', 'TxRef', TxRef)

        OrgnlTxNode = doc.createElement('ns4:OrgnlTx')
        Tx.appendChild(OrgnlTxNode)
        TxIdNode = doc.createElement('ns4:TxId')
        OrgnlTxNode.appendChild(TxIdNode)
        self.add_element(doc, TxIdNode, 'ns4', 'TxDtTm', TxDtTmNode)
        self.add_element(doc, TxIdNode, 'ns4', 'TxRef', TxRefNode)

        POINode = doc.createElement('ns4:POIId')
        OrgnlTxNode.appendChild(POINode)
        self.add_element(doc, POINode, 'ns4', 'Id', POI_id)
        self.add_element(doc, OrgnlTxNode, 'ns4', 'TxTp', 'CRDP')

        TxRslt = doc.createElement('ns4:TxRslt')
        OrgnlTxNode.appendChild(TxRslt)
        RspnToAuthstn = doc.createElement('ns4:RspnToAuthstn')
        TxRslt.appendChild(RspnToAuthstn)
        self.add_element(doc, RspnToAuthstn, 'ns4', 'Rspn', 'APPR')
        self.add_element(doc, TxRslt, 'ns4', 'AuthstnCd', AuthstnCd)

        TxDtls = doc.createElement('ns4:TxDtls')
        Tx.appendChild(TxDtls)
        self.add_element(doc, TxDtls, 'ns4', 'Ccy', str(Ccy))
        self.add_element(doc, TxDtls, 'ns4', 'TtlAmt', str(TtlAmt))

        SctyTrlr = doc.createElement('ns4:SctyTrlr')
        AccptrCxlReq.appendChild(SctyTrlr)
        self.add_element(doc, SctyTrlr, 'ns4', 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorCancellationRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))

    def AcceptorRefundRequest(self, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxDtTmNode, TxRefNode, Ccy, TtlAmt, PdctCd, PdctQty, UnitPric, PdctAmt):
        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorRefundRequest = doc.createElement('AcceptorRefundRequest')
        AcceptorRefundRequest.setAttribute('xmlns', 'http://schemas.bssys.com/iso20022/service/messages/v1')
        
        AccptrRfndReq = doc.createElement('AccptrRfndReq')
        AccptrRfndReq.setAttribute('xmlns', 'urn:iso:std:iso:20022:tech:xsd:caaa.016.001.01')
        AcceptorRefundRequest.appendChild(AccptrRfndReq)

        Hdr = doc.createElement('Hdr')
        AccptrRfndReq.appendChild(Hdr)
        self.create_element(doc, Hdr, 'PrtcolVrsn', '01.00')
        self.create_element(doc, Hdr, 'XchgId', '1')
        self.create_element(doc, Hdr, 'CreDtTm', datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00')

        InitgPtyNode = doc.createElement('InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.create_element(doc, InitgPtyNode, 'Id', InitgPty)

        RfndReq = doc.createElement('RfndReq')
        AccptrRfndReq.appendChild(RfndReq)
        Envt = doc.createElement('Envt')
        RfndReq.appendChild(Envt)

        MrchntNode = doc.createElement('Mrchnt')
        Envt.appendChild(MrchntNode)
        MrchntIdNode = doc.createElement('Id')
        MrchntNode.appendChild(MrchntIdNode)
        self.create_element(doc, MrchntIdNode, 'Id', Mrchnt)

        POI = doc.createElement('POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('Id')
        POI.appendChild(POIIdNode)
        self.create_element(doc, POIIdNode, 'Id', POI_id)

        Card = doc.createElement('Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('PlainCardData')
        Card.appendChild(PlainCardData)
        self.create_element(doc, PlainCardData, 'PAN', PAN)
        self.create_element(doc, PlainCardData, 'XpryDt', XpryDt)
        self.create_element(doc, Card, 'CardPdctPrfl', '0060')
        self.create_element(doc, Card, 'AddtlCardData', AddtlCardData)

        Cntxt = doc.createElement('Cntxt')
        RfndReq.appendChild(Cntxt)
        PmtCntxt = doc.createElement('PmtCntxt')
        Cntxt.appendChild(PmtCntxt)
        self.create_element(doc, PmtCntxt, 'CardDataNtryMd', 'BRCD')
        SaleCntxt = doc.createElement('SaleCntxt')
        Cntxt.appendChild(SaleCntxt)

        Tx = doc.createElement('Tx')
        RfndReq.appendChild(Tx)
        self.create_element(doc, Tx, 'TxCaptr', 'true')
        self.create_element(doc, Tx, 'MrchntCtgyCd', '5411')

        TxId = doc.createElement('TxId')
        Tx.appendChild(TxId)
        self.create_element(doc, TxId, 'TxDtTm', TxDtTm)
        self.create_element(doc, TxId, 'TxRef', TxRef)

        OrgnlTx = doc.createElement('OrgnlTx')
        Tx.appendChild(OrgnlTx)
        TxIdNode = doc.createElement('TxId')
        OrgnlTx.appendChild(TxIdNode)
        self.create_element(doc, TxIdNode, 'TxDtTm', TxDtTmNode)
        self.create_element(doc,TxIdNode, 'TxRef', TxRefNode)

        POIId = doc.createElement('POIId')
        OrgnlTx.appendChild(POIId)
        self.create_element(doc, POIId, 'Id', POI_id)

        MrchntId = doc.createElement('MrchntId')
        OrgnlTx.appendChild(MrchntId)
        self.create_element(doc, MrchntId, 'Id', Mrchnt)
        self.create_element(doc, OrgnlTx, 'TxTp', 'CRDP')

        TxRslt = doc.createElement('TxRslt')
        OrgnlTx.appendChild(TxRslt)
        self.create_element(doc, TxRslt, 'Rspn', 'APPR')

        TxDtls = doc.createElement('TxDtls')
        Tx.appendChild(TxDtls)
        self.create_element(doc, TxDtls, 'Ccy', str(Ccy))
        self.create_element(doc, TxDtls, 'TtlAmt', str(TtlAmt))

        Pdct = doc.createElement('Pdct')
        TxDtls.appendChild(Pdct)
        self.create_element(doc, Pdct, 'PdctCd', PdctCd)
        self.create_element(doc, Pdct, 'UnitOfMeasr', 'PIEC')
        self.create_element(doc, Pdct, 'PdctQty', PdctQty)
        self.create_element(doc, Pdct, 'UnitPric', UnitPric)
        self.create_element(doc, Pdct, 'PdctAmt', PdctAmt)

        SctyTrlr = doc.createElement('SctyTrlr')
        AccptrRfndReq.appendChild(SctyTrlr)
        self.create_element(doc, SctyTrlr, 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorRefundRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))