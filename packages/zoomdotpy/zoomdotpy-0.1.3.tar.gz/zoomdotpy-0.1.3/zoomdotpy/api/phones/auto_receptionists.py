from ..base import _BaseAPI

class AutoReceptionistsAPI(_BaseAPI):
    def list_auto_receptionists(self, params: dict):
        """
            Use this API to list auto receptionists.
			
			**Prerequisites:**
			* Pro or a higher account with Zoom Phone license.
			* Account owner or admin permissions.
			
			**Scopes:** `phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        res = self.request(
            'GET',
            f'/phone/auto_receptionists',
            params=params
        )

        return res.json()

    def create_auto_receptionists(
        self, 
        auto_receptionist_name: str, 
        site_id: str
    ):
        """
            Auto receptionists answer calls with a personalized recording and routes calls to a phone user, call queue, common area phone, voicemail or an IVR system. Use this API to add an [auto receptionist](https://support.zoom.us/hc/en-us/articles/360021121312-Managing-Auto-Receptionists-and-Interactive-Voice-Response-IVR-) to a Zoom Phone
			
			**Prerequisites:**
			* Pro or higher account with Zoom Phone license.
			* Account owner or admin privileges 
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        body = {
            'name'      : auto_receptionist_name,
            'site_id'   : site_id
        }

        res = self.request(
            'POST',
            f'/phone/auto_receptionists',
            json=body
        )

        return res.json()
    
    def get_auto_receptionist(self, auto_receptionist_id: str):
        """
            Use this API to get information on a specific auto receptionist.
			
			**Prerequisites:**
			* Pro or a higher account with Zoom Phone license.
			* Account owner or admin permissions.
			
			**Scopes:** `phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        res = self.request(
            'GET',
            f'/phone/auto_receptionists/{auto_receptionist_id}'
        )

        return res.json()

    def update_auto_receptionist(
        self, 
        auto_receptionist_id    : str,
        cost_center             : str = None,
        department              : str = None,
        extension_number        : int = None,
        auto_receptionist_name  : str = None,
        audio_prompt_language   : str = None,
        timezone                : str = None
    ):
        """
            An auto receptionist answers calls with a personalized recording and routes calls to a phone user, call queue, common area phone, or voicemail. An auto receptionist can also be set up so that it routes calls to an interactive voice response (IVR) system to allow callers to select the routing options.
			Use this API to [change information](https://support.zoom.us/hc/en-us/articles/360021121312-Managing-Auto-Receptionists-and-Interactive-Voice-Response-IVR-#h_1d5ffc56-6ba3-4ce5-9d86-4a1a1ee743f3) such as the display name and extension number assigned to the main auto receptionist.
			
			**Prerequisites:**
			* Pro or higher account with Zoom Phone license.
			
			**Scopes:** `phone:write:admin` 
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        body = {}
        
        if cost_center              : body['cost_center']           = cost_center
        if department               : body['department']            = department
        if extension_number         : body['extension_number']      = extension_number
        if auto_receptionist_name   : body['name']                  = auto_receptionist_name
        if audio_prompt_language    : body['audio_prompt_language'] = audio_prompt_language
        if timezone                 : body['timezone']              = timezone

        res = self.request(
            'PATCH',
            f'/phone/auto_receptionists/{auto_receptionist_id}',
            json=body
        )

        return res.json()

    def delete_auto_receptionist(self, auto_receptionist_id: str):
        """
            An auto receptionist answers calls with a personalized recording and routes calls to a phone user, call queue, common area (phone), or to a voicemail. An auto receptionist can also be set up so that it routes calls to an interactive voice response (IVR) system to allow callers to select the routing options.
			Use this API to [delete a non-primary auto receptionist](https://support.zoom.us/hc/en-us/articles/360021121312-Managing-Auto-Receptionists-and-Interactive-Voice-Response-IVR-#h_1d5ffc56-6ba3-4ce5-9d86-4a1a1ee743f3).
			
			**Prerequisites:**
			* Pro or higher account with Zoom Phone license.
			
			**Scopes:** `phone:write:admin` 
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'DELETE',
            f'/phone/auto_receptionists/{auto_receptionist_id}'
        )

        return res.json()