import re


async def input_verifier(**kwargs):
    bill_comm_err_dict = {
        "ERR_REQ_ARGS": "{}, command requires the following arguments: {}",
        "ERR_QUERY": "{}, please provide one query",
        "ERR_QUERY_TERM": "{}, please provide one query term",
        "ERR_INV_CAT": "{}, invalid song property"
    }

    ctx = kwargs['ctx']

    try:
        bill_item = kwargs['bill_item']

        args = ctx.content.split(" ", 1)
        regex = r"\"([^\"]*)\""

        if len(args) < 2:
            return await ctx.channel.send(bill_comm_err_dict["ERR_REQ_ARGS"].format(ctx.author.mention))

        query = re.findall(regex, args[1])

        if len(query) != 1:
            return await ctx.channel.send(bill_comm_err_dict["ERR_NO_QUERY"].format(ctx.author.mention))

        query_cln_spl = query[0].split(":")

        if len(query_cln_spl) != 2 or (len(query_cln_spl) > 2 and query_cln_spl[1].strip() == ""):
            return await ctx.channel.send(bill_comm_err_dict["ERR_QUERY_TERM"].format(ctx.author.mention))

        getattr(bill_item, query_cln_spl[0])

        query_category = query_cln_spl[0]
        query_item = query_cln_spl[1]

        return {"query_item": query_item, "query_category": query_category}
    except AttributeError:
        await ctx.channel.send(bill_comm_err_dict["ERR_INV_CAT"].format(ctx.author.mention))
    except Exception as e:
        raise BaseException(e)
