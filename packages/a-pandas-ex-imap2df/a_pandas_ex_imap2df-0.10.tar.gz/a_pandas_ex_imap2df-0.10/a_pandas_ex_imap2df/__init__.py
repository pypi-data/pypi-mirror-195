import imaplib
import email
import pandas as pd
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()


def imap2df(
    number,
    username,
    password,
    imap_server,
):
    df = pd.DataFrame()
    try:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        messages = int(messages[0])
        allresults = []
        for i in range(messages, messages - number, -1):
            try:
                res, msg = imap.fetch(str(i), "(RFC822)")
            except Exception:
                break
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    allresults.append(msg.__dict__.items())

        df = pd.DataFrame.from_records(allresults)
        df.columns = (
            "bb_policy",
            "aa_headers",
            "bb_unixfrom",
            "aa_content",
            "bb_charset",
            "bb_preamble",
            "bb_epilogue",
            "bb_defects",
            "aa_default_type",
        )
        for col in df.columns:
            df[col] = df[col].ds_apply_ignore(pd.NA, lambda x: x[1:])

        df = df.drop(columns="aa_default_type")
        df["aa_email_index"] = df.index.__array__().copy()
        df = df.drop(columns=[x for x in df.columns if "bb_" in x])
        df["aa_contentobj"] = df["aa_content"].copy()
        df = df.explode("aa_content").explode("aa_content").reset_index(drop=True)

        df["aa_content_inf"] = df["aa_content"].ds_apply_ignore(
            pd.NA, lambda xx: [x for x in xx.raw_items()]
        )
        df["aa_content_str"] = df.aa_content.ds_apply_ignore(pd.NA, str)
        df["aa_content_bytes"] = df.aa_content.ds_apply_ignore(
            pd.NA, lambda x: x.__bytes__()
        )
        df = (
            df.explode("aa_content_inf")
            .explode("aa_headers")
            .explode("aa_headers")
            .reset_index(drop=True)
        )
        df["aa_headers1"] = df.aa_headers.str[-1]
        df["aa_headers0"] = df.aa_headers.str[0]
        df["aa_content1"] = df.aa_content_inf.str[-1]
        df["aa_content0"] = df.aa_content_inf.str[0]
        df = df.filter(sorted(df.columns))
        df = df.drop(
            columns=["aa_content", "aa_content_inf", "aa_headers"]
        ).reset_index(drop=True)

    finally:
        try:
            imap.close()
            imap.logout()
        except Exception:
            pass
    return df


def pd_add_imap2df():
    pd.Q_imap2df = imap2df
