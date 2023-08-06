import copy
import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from enum import Enum

from dateutil.relativedelta import relativedelta

from .conn import IAMApi, IAMApiLegacy
from .utils import (
    check_password,
    format_leitzahl,
    format_notification,
    gen_password,
    to_date,
)
from .verbose import VERBOSE


class Notification(Enum):
    GH = "To guest and host"
    GHT = "To guest, host and technical contact"
    HT = "To host and technical contact"
    G = "To guest only"
    GT = "To guest and technical contact"
    H = "To host"
    T = "To technical contact"


map_iamfields2internal = {
    "displayname": "displayname",
    "employeetype": "type",
    "enddate": "end_date",
    "firstname": "firstname",
    "lastname": "familyname",
    "gender": "gender",
    "salutation": "title",
    "mail": "mail",
    "department": "department",
    "dateofbirth": "birth_date",
    "startdate": "start_date",
    "enddate": "end_date",
    "createtimestamp": "cre_date",
    "modifytimestamp": "mod_date",
    "npid": "npid",
    "nuid": "nuid",
    "persid": "persid",
    "uidnumber": "uidNumber",
    "gidnumber": "gidNumber",
    "orcid": "orcid",
    "userstate": "state",
    "username": "username",
    "category": "category",
    "perscattext": "category",
    "guesttechnicalcontact": "technical_contact",
    "host": "host_username",
    "hostorg": "host_leitzahl",
    "notification": "notification",
    "description": "description",
    "respadminrole": "host_admingroup",
}
map_internal2iamfields = {
    "host_username": "host",
    "host_leitzahl": "hostOrg",
    "host_admingroup": "respAdminRole",
}

map_iamlegacyfields2internal = {
    "firstname": "firstname",
    "familyname": "familyname",
    "title": "title",
    "description": "description",
    "email": "mail",
    "npid": "npid",
    "persid": "persid",
    "uidnumber": "uidNumber",
    "gidnumber": "gidNumber",
    "orcid": "orcid",
    "primary_perskat": "category",
    "primary_username": "username",
    "perskats": "perskats",
    "usernames": "usernames",
}

guest_properties_required = [
    "firstname",
    "lastname",
    "mail",
    "description",
    "dateofbirth",
    "hostorg",
    "host",
    "technicalcontact",
    "admingroup",
    "notification",
    "startdate",
    "enddate",
]

guest_properties_optional = [
    "title",
    "salutation",
    "ahvNo",
    "addressLine1",
    "addressLine2",
    "addressLine3",
    "postCode",
    "place",
    "countryName",
]

guest_properties_update = [
    "description",
    "hostOrg",
    "host",
    "guestTechnicalContact",
    "endDate",
    "notification",
    "respAdminRole",
    "deactivationStartDate",
    "deactivationEndDate",
]


@dataclass
class Person(IAMApi):
    firstname: str = None
    familyname: str = None
    gender: str = None
    displayname: str = None
    persid: int = None
    npid: int = None
    nuid: int = None
    gidNumber: int = None
    uidNumber: int = None
    username: str = None
    mail: str = None
    orcid: str = None
    description: str = None
    birth_date: str = None
    title: str = None
    type: str = None
    state: str = None
    cre_date: str = None
    start_date: str = None
    mod_date: str = None
    end_date: str = None
    category: str = None
    department: str = None

    @property
    def data(self):
        return asdict(self)

    def get_person(self, identifier):
        endpoint = f"/users/{identifier}"
        data = self.get_request(endpoint=endpoint)
        return self.new_from_data(data)

    def new_from_data(self, data):
        new_person = {}
        # print(json.dumps(data, indent=4))
        for data_field in data:
            if data_field.lower() in map_iamfields2internal:
                new_person[map_iamfields2internal[data_field.lower()]] = data[
                    data_field
                ]
            else:
                pass
        new_person["mail"] = new_person["mail"][0] if len(new_person["mail"]) else None
        new_person["category"] = (
            new_person["category"][0] if len(new_person["category"]) else None
        )
        for field in ("start_date", "end_date"):
            new_person[field] = (
                to_date(new_person[field]).strftime("%Y-%d-%m")
                if new_person[field]
                else None
            )

        person = Person(**new_person)
        person._admin_username = self._admin_username
        person._admin_password = self._admin_password
        # print(json.dumps(asdict(person), indent=4))
        return person

    def delete_user(self, username: str):
        endpoint = f"/users/{self.username}/personas/{username}"
        print(endpoint)
        self.delete_request(endpoint=endpoint)


@dataclass
class PersonLegacy(IAMApiLegacy):
    firstname: str = None
    familyname: str = None
    title: str = None
    description: str = None
    mail: str = None
    persid: int = None
    npid: int = None
    nuid: int = None
    gidNumber: int = None
    uidNumber: int = None
    orcid: str = None
    username: int = None
    usernames: list[dict] = field(default_factory=list)
    perskats: list[dict] = field(default_factory=list)
    category: str = None

    @property
    def data(self):
        return asdict(self)

    def get_persons(self, leitzahl: int = None):
        """Get persons via search item: leitzahl,"""

        endpoint = f"usermgr/person?leitzahl={leitzahl}"
        datas = self.get_request(endpoint)
        persons = []
        for data in datas:
            person = Person(**data)
            persons.append(person)
        return persons

    def new_from_data(self, data):
        new_person = {}
        for data_field in data:
            if data_field.lower() in map_iamlegacyfields2internal:
                new_person[map_iamlegacyfields2internal[data_field.lower()]] = data[
                    data_field
                ]
            else:
                pass

        person = PersonLegacy(**new_person)
        person._admin_username = self._admin_username
        person._admin_password = self._admin_password
        return person

    def get_person(self, identifier: str):
        """Get person via identifier (username, email, npid)"""
        endpoint = f"usermgr/person/{identifier}"
        data = self.get_request(endpoint)
        return self.new_from_data(data)

    def save(self):
        body = {
            key: getattr(self, key, None)
            for key in guest_properties_required + guest_properties_optional
        }
        if self.is_new:
            endpoint = "usermgr/person/"
            resp = self.conn._post_request(endpoint, body)
            action = "created"
        else:
            endpoint = f"usermgr/person/{self.npid}"
            resp = self.conn._put_request(endpoint, body)
            action = "updated"

        if resp.ok:
            # TODO: get the new npid from post request?
            if VERBOSE:
                print(
                    f"Person {self.firstname} {self.familyname} was successfully {action}"
                )
        elif resp.status_code == 401:
            raise ValueError(
                "the provided admin-username/password is incorrect or you are not allowed to create/update this person"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(f"unable to create/update this person: {data['message']}")

    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))

    def new_user(
        self,
        username,
        password=None,
        firstname=None,
        familyname=None,
        mail=None,
        description=None,
    ):
        if len(username) < 6:
            raise ValueError("Usernames must be 6 chars or longer")
        if password is None:
            password = gen_password()
        elif not check_password(password):
            raise ValueError(
                "the initial password must contain at least Lowercase, uppercase characters and a digit"
            )
        if description is None:
            description = username
        endpoint = "usermgr/person/{}".format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body)
        if resp.ok:
            user = self.conn.get_user(username)
            user.init_password = password
            if VERBOSE:
                print("new user {} was successfully created".format(username))
            return user
        elif resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data["message"])


class GuestOld:
    def __init__(self, conn, data=None, is_new=False):
        self.date_fields = [
            "startDate",
            "endDate",
            "deactivationStartDate",
            "deactivationEndDate",
            "dateOfBirth",
        ]
        self.conn = conn
        self.is_new = is_new
        if data:
            self._set_data(data)

    def _set_data(self, data):
        for key in data:
            if key in self.date_fields:
                d = to_date(data[key])
                data[key] = d
        self.data = data

    def _server_body(self):
        """Transform data to be send to the server"""
        body = copy.deepcopy(self.data)
        for date_field in self.date_fields:
            if date_field in body:
                if body[date_field]:
                    body[date_field] = body[date_field].strftime("%d.%m.%Y")
        return body

    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))

    def save(self):
        endpoint = "/guests"
        hostname = self.conn.hostname_new
        endpoint_base = self.conn.endpoint_base_new

        if self.is_new:
            resp = self.conn._post_request(
                endpoint,
                self._server_body(),
                hostname=hostname,
                endpoint_base=endpoint_base,
            )
            if resp.ok:
                guest_info = json.loads(resp.content.decode())
                self._set_data(guest_info)
                if VERBOSE:
                    print(
                        f"Guest successfully created with username: {self.data['username']}"
                    )

        else:
            endpoint += f"/{self.data['username']}"
            resp = self.conn._put_request(
                endpoint,
                self._server_body(),
                hostname=hostname,
                endpoint_base=endpoint_base,
            )
            if resp.ok:
                if VERBOSE:
                    print(f"Guest successfully updated.")
                guest_info = json.loads(resp.content.decode())
                self._set_data(guest_info)

        if resp.status_code == 401:
            raise ValueError(
                "Provided admin-username/password is incorrect or you are not allowed to do this operation"
            )
        elif not resp.ok:
            if resp.content:
                raise ValueError(f"{resp.status_code}: {resp.content}")
            else:
                raise ValueError(f"got status: {resp.status_code}")


@dataclass
class Guest(Person):
    host_username: int = None
    host_leitzahl: int = None
    host_admingroup: str = None
    notification: Notification = Notification.GH.value
    technical_contact: str = None
    admingroup: str = None

    @classmethod
    def new_from_data(self, data):
        new_guest = {}
        for data_field in data:
            if data_field.lower() in map_iamfields2internal:
                new_guest[map_iamfields2internal[data_field.lower()]] = data[data_field]
            else:
                pass

        for date_field in ("start_date", "end_date"):
            if date_field in new_guest:
                new_guest[date_field] = to_date(new_guest[date_field]).strftime(
                    "%Y-%m-%d"
                )
        new_guest["mail"] = new_guest["mail"][0] if len(new_guest["mail"]) else None

        guest = Guest(**new_guest)
        guest._admin_username = self._admin_username
        guest._admin_password = self._admin_password
        return guest

    def get_guest(self, identifier):
        endpoint = f"/guests/{identifier}"
        data = self.get_request(endpoint=endpoint)
        return Guest.new_from_data(data)

    def get_guests(
        self,
        host_username: str = None,
        host_leitzahl: str = None,
        host_admingroup: str = None,
    ):
        query = "&".join(
            [
                f"{map_internal2iamfields[k]}={v}"
                for k, v in locals().items()
                if v is not None and k != "self"
            ]
        )
        endpoint = f"/guests?{query}"
        datas = self.get_request(endpoint=endpoint)
        guests = []
        for data in datas:
            guests.append(Guest.new_from_data(data))
        return guests

    def extend(self, username: str, end_date=None, months=None):
        if end_date:
            end_date = to_date(end_date)
        elif months:
            today = date.today()
            end_date = today + relativedelta(months=int(months))
        else:
            today = date.today()
            end_date = today + relativedelta(months=12)
        body = {"endDate": end_date.strftime("%d.%m.%Y")}

        endpoint = f"/guests/{username}"
        data = self.put_request(endpoint=endpoint, body=body)
        return Guest.new_from_data(data)

    def update(
        self,
        username,
        description: str = None,
        host_username: str = None,
        host_admingroup: str = None,
        host_leitzahl: str = None,
        technical_contact: str = None,
        notification: Notification = Notification.GH.value,
        end_date: str = None,
        deactivation_start_date: str = None,
        deactivation_end_date: str = None,
    ):
        payload = {}
        if host_username:
            payload["host"] = host_username
        if host_admingroup:
            payload["respAdminRole"] = host_admingroup
        if description:
            payload["description"] = description
        if technical_contact:
            payload["guestTechnicalContact"] = technical_contact
        if notification:
            notification = format_notification(notification)
            payload["notification"] = notification
        if host_leitzahl:
            payload["hostOrg"] = host_leitzahl
        if end_date:
            payload["endDate"] = to_date(end_date).strftime("%Y-%m-%d")
        if deactivation_start_date is not None:
            payload["deactivationStartDate"] = to_date(
                deactivation_start_date
            ).strftime("%Y-%m-%d")
        if deactivation_end_date is not None:
            payload["deactivationEndDate"] = to_date(deactivation_end_date).strftime(
                "%Y-%m-%d"
            )

        endpoint = f"/guests/{username}"
        data = self.put_request(endpoint=endpoint, body=payload)
        return Guest.new_from_data(data)

    def create(
        self,
        firstname: str,
        familyname: str,
        mail: str,
        host_username: str,
        host_admingroup: str,
        host_leitzahl: str = None,
        description=None,
        birth_date: str = None,
        technical_contact: str = None,
        notification: str = None,
        start_date: str = None,
        end_date: str = None,
        salutation=None,
        ahvNo=None,
        address_line1: str = None,
        address_line2: str = None,
        address_line3: str = None,
        postcode: str = None,
        place: str = None,
        country: str = None,
    ):
        if birth_date is None:
            birth_date = date(2000, date.today().month, date.today().day)
        if start_date is None:
            start_date = date.today()
        else:
            start_date = to_date(start_date)
        if not end_date:
            end_date = start_date + relativedelta(days=365)
        elif (end_date - start_date).days > 365:
            raise ValueError(
                "Difference between endDate and startDate is more than 356 days."
            )

        host_person = self.get_person(host_username)
        if not host_person:
            user = self.get_user(host_username)
            host_person = self.get_person(user["npid"])
        if not host_person:
            print(f"no such host: {host_username}")

        if host_leitzahl is None:
            try:
                for perskat in host_person["perskats"]:
                    if perskat["perskat"] == "Mitarbeiter":
                        host_leitzahl = perskat["leitzahl"]
                        break
            except Exception:
                pass
        if host_leitzahl is None:
            raise ValueError("no host leitzahl for guest provided.")
        if technical_contact is None:
            try:
                technical_contact = host_person["email"]
            except Exception:
                pass
            if not technical_contact:
                raise ValueError("no mail for guestTechnicalContact found.")
        if notification is None:
            notification = "gh"
        else:
            notification = format_notification(notification)

        body = {
            "firstName": firstname,
            "lastName": familyname,
            "mail": mail,
            "host": host_username,
            "respAdminRole": host_admingroup,
            "description": f"guest of {host_username}"
            if description is None
            else description,
            "dateOfBirth": birth_date.strftime("%d.%m.%Y"),
            "guestTechnicalContact": technical_contact,
            "notification": notification,
            "hostOrg": host_leitzahl,
            "startDate": start_date.strftime("%d.%m.%Y"),
            "endDate": end_date.strftime("%d.%m.%Y"),
            "salutation": salutation,
            "ahvNo": ahvNo,
            "addressLine1": address_line1,
            "addressLine2": address_line2,
            "addressLine3": address_line3,
            "postCode": postcode,
            "place": place,
            "countryName": country,
        }
        endpoint = "/guests"
        data = self.post_request(endpoint=endpoint, body=body)
        guest = Guest.new_from_data(data)
        guest._admin_username = self._admin_username
        guest._admin_password = self._admin_password
        return guest
