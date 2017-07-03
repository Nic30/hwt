from hwt.serializer.serializerClases.indent import getIndent


class SystemCSerializer_statements():
    @classmethod
    def HWProcess(cls, proc, ctx):
        """
        Serialize HWProcess instance

        :param scope: name scope to prevent name collisions
        """
        body = proc.statements

        def createTmpVarFn(suggestedName, dtype):
            raise NotImplementedError()

        childCtx = ctx.withIndent()
        statemets = [cls.asHdl(s, childCtx) for s in body]
        proc.name = ctx.scope.checkedName(proc.name, proc)

        return cls.methodTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            statements=statemets
            )
        
        
    
    @classmethod
    def IfContainer(cls, ifc, ctx):
        """
        Serailize IfContainer instance
        """
        cond = cls.condAsHdl(ifc.cond, True, ctx)
        elIfs = []

        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse

        childCtx = ctx.withIndent()
        def s(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        for c, statements in ifc.elIfs:
            elIfs.append((cls.condAsHdl(c, True, ctx), s(statements)))

        return cls.IfTmpl.render(
                            indent=getIndent(ctx.indent),
                            cond=cond,
                            ifTrue=s(ifTrue),
                            elIfs=elIfs,
                            ifFalse=s(ifFalse))