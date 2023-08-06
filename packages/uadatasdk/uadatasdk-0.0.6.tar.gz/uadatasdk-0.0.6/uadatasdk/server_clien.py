api_description = """
service PingPong {
    string query(1:string method_name,2: binary params),
    map<string,string> auth(1: string name,2: string password),
}
"""

import thriftpy2
import six

pingpong_thrift = thriftpy2.load_fp(six.StringIO(api_description),module_name="pingpong_thrift")



