int main(){
    int x;
    int y;
    int z;

    // pre-conditions
    x = 0;
    y = 200;
    z = 400;

    // loop body
    while(unknown()){
        if(x < 200){
            y = y + 1;
        }else{
            z = z + 2;
        }   
        x = x + 1;
    }

    // post-condition
    if(y >= 400){
        assert(z == 2 * x);
    }
    
}