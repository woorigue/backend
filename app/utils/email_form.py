def verify_email_form(code: str):
    verify_email_form = f"""
<!DOCTYPE html>
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="UTF-8" />
    <title>이메일 인증</title>
  </head>
  <body
    style="
      max-width: 600px;
      margin: 0 auto;
      padding: 0;
      background-color: #f9f9f9;
    ">
    <div style="margin: 0 auto; background-color: white">
      <div
        style="
          background-color: #3d9bff;
          padding-top: 40px;
          padding-bottom: 40px;
          text-align: center;
        ">
        <img
          src="https://i.ibb.co/L8p6CHp/logo-white.png"
          alt="logo-white"
          border="0"
          style="width: 60px" />
      </div>

      <div style="text-align: left">
        <div style="padding-right: 40px; padding-left: 40px; margin-top: 40px">
          <h3 style="color: #333">비밀번호 초기화 인증코드</h3>
          <p style="color: #444; font-size: 16px; line-height: 1.6">
            안녕하세요, 우리에서 요청하신 인증번호를 보내드립니다.
          </p>
          <p style="color: #444; font-size: 16px; line-height: 1.6">
            비밀번호 초기화를 위해서는 본인확인을 위해 인증번호 확인이
            필요합니다.<br />

            아래의 인증번호 5자리를 인증번호 입력창에 입력해주세요.<br />

            인증번호는 발송된 시점부터 3분간 유효하니 확인 후 입력해 주시기
            바랍니다.
          </p>
        </div>

        <div
          style="
            background-color: #d6eeff;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            margin: 30px 0;
          ">
          <span
            style="
              font-size: 28px;
              color: #3d9bff;
              letter-spacing: 6px;
              font-weight: bold;
            ">
            {code}
          </span>
        </div>

        <div
          style="
            padding-right: 40px;
            padding-left: 40px;
            margin-top: 40px;
            margin-bottom: 40px;
          ">
          <p style="color: #666; font-size: 12px; line-height: 1.6">
            본 메일은 발신전용이므로 본 메일로 회신하실 경우 답변이
            되지않으며,<br />

            서비스 이용 안내메일로 수신동의 여부와 관계없이 발송되었습니다.
          </p>
        </div>
      </div>

      <div style="padding: 20px; text-align: center; background-color: #f2f2f2">
        <p style="color: #888; font-size: 12px">
          본 메일은 발신전용이므로 회신되지 않습니다.
        </p>
        <a
          href="https://woori-three.vercel.app/"
          style="color: #888; text-decoration: underline; font-size: 12px">
          사이트 바로가기
        </a>
      </div>
    </div>
  </body>
</html>
    """
    return verify_email_form


def sign_up_form(code: str) -> str:
    data = f"""
<!DOCTYPE html>
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="UTF-8" />
    <title>이메일 인증</title>
  </head>
  <body
    style="
      max-width: 600px;
      margin: 0 auto;
      padding: 0;
      background-color: #f9f9f9;
    ">
    <div style="margin: 0 auto; background-color: white">
      <div
        style="
          background-color: #3d9bff;
          padding-top: 40px;
          padding-bottom: 40px;
          text-align: center;
        ">
        <img
          src="https://i.ibb.co/L8p6CHp/logo-white.png"
          alt="logo-white"
          border="0"
          style="width: 60px" />
      </div>

      <div style="text-align: left">
        <div style="padding-right: 40px; padding-left: 40px; margin-top: 40px">
          <h3 style="color: #333">회원가입을 환영합니다!</h3>
          <p style="color: #444; font-size: 16px; line-height: 1.6">
            안녕하세요, 우리에서 요청하신 인증번호를 보내드립니다.
          </p>
          <p style="color: #444; font-size: 16px; line-height: 1.6">
            회원가입을 위해서는 본인확인을 위해 인증번호 확인이 필요합니다.<br />

            아래의 인증번호 5자리를 인증번호 입력창에 입력해주세요.<br />

            인증번호는 발송된 시점부터 3분간 유효하니 확인 후 입력해 주시기
            바랍니다.
          </p>
        </div>

        <div
          style="
            background-color: #d6eeff;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            margin: 30px 0;
          ">
          <span
            style="
              font-size: 28px;
              color: #3d9bff;
              letter-spacing: 6px;
              font-weight: bold;
            ">
            {code}
          </span>
        </div>

        <div
          style="
            padding-right: 40px;
            padding-left: 40px;
            margin-top: 40px;
            margin-bottom: 40px;
          ">
          <p style="color: #666; font-size: 12px; line-height: 1.6">
            본 메일은 발신전용이므로 본 메일로 회신하실 경우 답변이
            되지않으며,<br />

            서비스 이용 안내메일로 수신동의 여부와 관계없이 발송되었습니다.
          </p>
        </div>
      </div>

      <div style="padding: 20px; text-align: center; background-color: #f2f2f2">
        <p style="color: #888; font-size: 12px">
          본 메일은 발신전용이므로 회신되지 않습니다.
        </p>
        <a
          href="https://woori-three.vercel.app/"
          style="color: #888; text-decoration: underline; font-size: 12px">
          사이트 바로가기
        </a>
      </div>
    </div>
  </body>
</html>
    """
    return data
