
import re
import socket

import hyperlink
from defusedxml import ElementTree as ET
from django.utils.html import escape, strip_tags
from dojo.models import Endpoint, Finding


class ZapParser(object):
    """Parser for xml file generated by the OWASP Zed Attacl Proxy (ZAP) tool https://www.zaproxy.org/."""

    def get_scan_types(self):
        return ["ZAP Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "ZAP Scan"

    def get_description_for_scan_types(self, scan_type):
        return "ZAP XML report format."

    def get_findings(self, xml_output, test):
        tree = ET.parse(xml_output)
        return self.get_items(tree, test)

    def get_items(self, tree, test):
        """
        @return items A list of Host instances
        """

        items = list()
        for node in tree.findall('site'):
            site = Site(node)
            main_host = Endpoint(host=site.host + (":" + site.port) if site.port is not None else "")
            if site.port and site.port.isdigit():
                main_host.port = int(site.port)
            for item in site.items:
                severity = item.riskdesc.split(' ', 1)[0]
                references = ''
                for ref in item.ref:
                    references += ref + "\n"

                find = Finding(
                    title=item.name,
                    cwe=item.cwe,
                    description=strip_tags(item.desc),
                    test=test,
                    severity=severity,
                    mitigation=strip_tags(item.resolution),
                    references=references,
                    false_p=False,
                    duplicate=False,
                    out_of_scope=False,
                    nb_occurences=1,
                )

                find.unsaved_endpoints = [main_host]
                for i in item.items:
                    parts = hyperlink.parse(i['uri'])
                    endpoint = Endpoint(
                        protocol=parts.scheme,
                        host=parts.host + (":" + str(parts.port) if parts.port is not None else ""),
                        port=parts.port,
                        path="/".join(parts.path),
                        query=parts.query,
                        fragment=parts.fragment,
                    )
                    find.unsaved_endpoints.append(endpoint)
                items.append(find)
        return items


def get_attrib_from_subnode(xml_node, subnode_xpath_expr, attrib_name):
    """
    Finds a subnode in the item node and the retrieves a value from it

    @return An attribute value
    """
    global ETREE_VERSION
    node = None

    if ETREE_VERSION[0] <= 1 and ETREE_VERSION[1] < 3:

        match_obj = re.search(r"([^\@]+?)\[\@([^=]*?)=\'([^\']*?)\'", subnode_xpath_expr)
        if match_obj is not None:
            node_to_find = match_obj.group(1)
            xpath_attrib = match_obj.group(2)
            xpath_value = match_obj.group(3)
            for node_found in xml_node.findall(node_to_find):
                if node_found.attrib[xpath_attrib] == xpath_value:
                    node = node_found
                    break
        else:
            node = xml_node.find(subnode_xpath_expr)

    else:
        node = xml_node.find(subnode_xpath_expr)

    if node is not None:
        return node.get(attrib_name)

    return None


class Site(object):
    def __init__(self, item_node):
        self.node = item_node
        self.name = self.node.get('name')
        self.host = self.node.get('host')
        self.name = self.node.get('name')
        self.port = self.node.get('port')
        self.items = []
        for alert in self.node.findall('alerts/alertitem'):
            self.items.append(Item(alert))

    def get_text_from_subnode(self, subnode_xpath_expr):
        """
        Finds a subnode in the host node and the retrieves a value from it.

        @return An attribute value
        """
        sub_node = self.node.find(subnode_xpath_expr)
        if sub_node is not None:
            return sub_node.text

        return None

    def resolve(self, host):
        try:
            return socket.gethostbyname(host)
        except:
            pass
        return host


class Item(object):
    """
    An abstract representation of a Item


    @param item_node A item_node taken from an zap xml tree
    """

    def __init__(self, item_node):
        self.node = item_node

        self.id = self.get_text_from_subnode('pluginid')
        self.name = self.get_text_from_subnode('alert')

        self.severity = self.get_text_from_subnode('riskcode')
        self.riskdesc = self.get_text_from_subnode('riskdesc')
        self.desc = self.get_text_from_subnode('desc')
        self.resolution = self.get_text_from_subnode('solution') if self.get_text_from_subnode('solution') else ""
        self.desc += "\n\nReference: " + self.get_text_from_subnode('reference') if self.get_text_from_subnode(
            'reference') else ""
        self.ref = []
        if self.get_text_from_subnode('cweid'):
            self.ref.append("CWE-" + self.get_text_from_subnode('cweid'))
            self.cwe = self.get_text_from_subnode('cweid')
        else:
            self.cwe = 0

        description_detail = "\n"
        for instance in item_node.findall('instances/instance'):
            for node in instance.iter():
                if node.tag == "uri":
                    if node.text != "":
                        description_detail += "URL: " + node.text
                if node.tag == "method":
                    if node.text != "":
                        description_detail += "Method: " + node.text
                if node.tag == "param":
                    if node.text != "":
                        description_detail += "Parameter: " + node.text
                if node.tag == "evidence":
                    if node.text != "":
                        description_detail += "Evidence: " + escape(node.text)
                description_detail += "\n"

        self.desc += description_detail

        if self.get_text_from_subnode('wascid'):
            self.ref.append("WASC-" + self.get_text_from_subnode('wascid'))

        self.items = []

        for instance in item_node.findall('instances/instance'):
            n = instance.findtext("uri")
            n2 = instance.findtext("param")
            url = hyperlink.parse(n)
            item = {'uri': n, 'param': n2 if n2 else "", 'host': url.host, 'protocol': url.scheme, 'port': url.port}
            self.items.append(item)

        self.requests = "\n".join([i['uri'] for i in self.items])

    def get_text_from_subnode(self, subnode_xpath_expr):
        """
        Finds a subnode in the host node and the retrieves a value from it.

        @return An attribute value
        """
        sub_node = self.node.find(subnode_xpath_expr)
        if sub_node is not None:
            return sub_node.text

        return None
